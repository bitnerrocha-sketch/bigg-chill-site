#!/usr/bin/env python3
"""
Bigg Chill Flavor Icon Processor
Converts source images to 384x384 transparent RGBA WebP icons.

Usage:
  python3 process_icons.py \
    --src "/path/to/source/folder" \
    --dst "/Users/alexrocha/bigg-chill-site/public/flavor-icons" \
    --map "campfire-delight:campfire delight.png,dark-chocolate:Dark chocolate.png"

  --map format: "output-name:source-filename" pairs, comma-separated
  Output name should be the kebab-case flavor name (without .webp extension)
"""

import argparse
import os
import sys
from PIL import Image
import numpy as np


TARGET_SIZE = (384, 384)
TARGET_MODE = "RGBA"
QUALITY = 90


def process_icon(src_path: str, dst_path: str) -> dict:
    """
    Convert a source image to a transparent 384x384 RGBA WebP.
    White background is removed — white pixels become transparent,
    black lines remain fully opaque. Matches the style of all existing
    Bigg Chill flavor icons.
    """
    img = Image.open(src_path).convert("RGBA")
    img = img.resize(TARGET_SIZE, Image.LANCZOS)
    data = np.array(img, dtype=np.float32)

    # Use inverse brightness as alpha:
    # white (255,255,255) → alpha 0 (fully transparent)
    # black (0,0,0)       → alpha 255 (fully opaque)
    brightness = (data[:, :, 0] + data[:, :, 1] + data[:, :, 2]) / 3.0
    new_alpha = (255 - brightness).clip(0, 255).astype(np.uint8)

    result = np.zeros((TARGET_SIZE[0], TARGET_SIZE[1], 4), dtype=np.uint8)
    result[:, :, 3] = new_alpha  # RGB stays 0 (black), only alpha varies

    out = Image.fromarray(result, TARGET_MODE)
    out.save(dst_path, "WEBP", quality=QUALITY)

    # Verification
    corner_alpha = out.getpixel((0, 0))[3]
    size = out.size
    mode = out.mode

    return {
        "path": dst_path,
        "size": size,
        "mode": mode,
        "corner_alpha": corner_alpha,
        "ok": size == TARGET_SIZE and mode == TARGET_MODE and corner_alpha <= 5,
    }


def main():
    parser = argparse.ArgumentParser(description="Process Bigg Chill flavor icons")
    parser.add_argument("--src", required=True, help="Source folder containing input images")
    parser.add_argument("--dst", required=True, help="Destination folder (public/flavor-icons)")
    parser.add_argument(
        "--map",
        required=True,
        help='Comma-separated "output-name:source-filename" pairs. '
             'Example: "campfire-delight:campfire.png,dark-chocolate:dark choc.png"',
    )
    args = parser.parse_args()

    pairs = [p.strip() for p in args.map.split(",")]
    errors = []

    print(f"\nProcessing {len(pairs)} icon(s)...\n")

    for pair in pairs:
        if ":" not in pair:
            print(f"  ⚠️  Skipping invalid pair (no colon): {pair}")
            continue

        out_name, src_name = pair.split(":", 1)
        out_name = out_name.strip()
        src_name = src_name.strip()

        src_path = os.path.join(args.src, src_name)
        dst_path = os.path.join(args.dst, f"{out_name}.webp")

        if not os.path.isfile(src_path):
            msg = f"Source file not found: {src_path}"
            print(f"  ❌  {out_name}: {msg}")
            errors.append(msg)
            continue

        try:
            result = process_icon(src_path, dst_path)
            status = "✅" if result["ok"] else "⚠️ "
            print(
                f"  {status}  {out_name}.webp — "
                f"size={result['size']}, mode={result['mode']}, "
                f"corner_alpha={result['corner_alpha']}"
            )
            if not result["ok"]:
                errors.append(f"{out_name}: unexpected output — {result}")
        except Exception as e:
            print(f"  ❌  {out_name}: {e}")
            errors.append(str(e))

    print()
    if errors:
        print(f"Completed with {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("All icons processed successfully.")


if __name__ == "__main__":
    main()
