---
name: bigg-chill-menu-update
description: >
  Use this skill whenever updating The Bigg Chill ice cream website menu.
  Triggers include "new menu from the client", "menu update", "update the flavors",
  "client sent a new menu", "add/remove flavors", "menu changes", or any time the
  client sends a new PDF or Word doc with ice cream flavors. This skill manages the
  full end-to-end workflow — comparing old vs new menus from PDFs or Word docs,
  identifying added/removed flavors and allergen changes, scanning all website files
  for affected code, generating an approval report, making all code edits across
  menu.astro and index.astro, processing and optimizing new flavor icons to match
  site specs, and running a thorough pre-publish audit. Always use this skill for
  any menu-related changes to The Bigg Chill website — do not attempt menu updates
  without it.
---

# Bigg Chill Menu Update Workflow

End-to-end process for updating The Bigg Chill ice cream website menu. Follow all steps in order. Pause for user approval at marked checkpoints — never skip them.

---

## Site Context

**Stack:** Astro static site  
**Repo:** `/Users/alexrocha/bigg-chill-site`

**Files that contain menu data:**
| File | What it contains |
|---|---|
| `src/pages/menu.astro` | `currentFlavors`, `dairyFreeFlavors`, `illustrationMap` |
| `src/pages/index.astro` | `flavors` array (homepage ticker, ~line 72) |

**Flavor icon specs:**
- Location: `public/flavor-icons/`
- Format: WebP, 384×384px, RGBA
- Background: transparent (white removed, alpha = 0)
- Naming: kebab-case (e.g. `birthday-cake.webp`)

**Flavor categories:**
- `Classic` — permanent core flavors
- `Limited Edition` — rotating seasonal
- `Boozy Delight` — alcohol-infused
- `Dairy-Free` — coconut milk base, plant-based

**Allergen tag values used in code:**
- `"Gluten-Friendly"` — gluten-free badge
- `"Nut-Free"` — nut-free badge
- `"Dairy-Free"` — dairy-free badge
- `"Plant-Based"` — plant-based badge

---

## Step 1 — Extract the Current Menu from Code

Read `src/pages/menu.astro` and extract the full `currentFlavors` array. Build a clean list of every flavor: name, category, and tags. This is the baseline for comparison.

---

## Step 2 — Parse the New Menu from Client Document

The client delivers the new menu as a PDF or Word doc. Read the file and extract for each flavor:
- Name
- Description
- Which allergen icons are shown (Gluten-Free, Nut-Free, Dairy-Free, Plant-Based)

A flavor with both Dairy-Free and Plant-Based icons is a Dairy-Free category flavor.

---

## Step 3 — Compare and Present the Diff

⛔ **CHECKPOINT — Wait for user confirmation before proceeding.**

Present a structured diff report:

**✅ FLAVORS TO ADD** (in new menu, not in current)
For each: name, description, allergen tags, suggested category

**❌ FLAVORS TO REMOVE** (in current menu, not in new)
For each: name only

**🔄 ALLERGEN CHANGES** (same flavor, different badges)
For each: name, old tags → new tags

Ask the user to confirm the diff is accurate. They may correct category assignments or other details before you proceed.

---

## Step 4 — Scan Code and Present Affected Lines Report

⛔ **CHECKPOINT — Present this report and wait for approval before making any edits.**

Search every source file and identify exactly what will change:

For **`src/pages/menu.astro`**, extract the specific object blocks for:
- Entries to remove from `currentFlavors`
- Entries to remove from `dairyFreeFlavors`
- Keys to remove from `illustrationMap`
- New entries to add to each

For **`src/pages/index.astro`**, show the current `flavors` array and which strings will be removed/added.

For **`public/flavor-icons/`**, list:
- Icon files to **add** (new flavors needing icons)
- Icon files to **delete** (removed flavors)

Present the full report. Get explicit approval before touching any code.

---

## Step 5 — Make All Code Changes

### `src/pages/menu.astro`

**Removing flavors:**
- Delete the full object entry from `currentFlavors`
- Delete the corresponding key from `illustrationMap`
- Delete from `dairyFreeFlavors` if present

**Adding flavors:**
Use this exact structure in `currentFlavors`, grouped with others of the same category:

```typescript
{
  name: "Flavor Name",
  description: "Description from client menu.",
  category: "Classic" | "Limited Edition" | "Boozy Delight" | "Dairy-Free",
  illustration: "camelCaseKey",
  tags: ["Gluten-Friendly", "Nut-Free"], // only include tags that apply
},
```

Add to `illustrationMap`:
```typescript
camelCaseKey: "/flavor-icons/kebab-case-name.webp",
```

If Dairy-Free category, also add to `dairyFreeFlavors`:
```typescript
{
  name: "Flavor Name",
  description: "Description.",
  illustration: "camelCaseKey",
  tags: ["Dairy-Free", "Plant-Based"],
},
```

**Updating allergens:** For any flavor whose badges changed, update the `tags` array accordingly.

**camelCase key convention:**
- "Dark Chocolate" → `darkChocolate`
- "London Fog" → `londonFog`
- "Chocolate Mousse Pie" → `chocolateMoussePie`
- "Campfire Delight" → `campfireDelight`
- Remove spaces, capitalize each word after the first

### `src/pages/index.astro`

Update the `flavors` array (~line 72):
- Remove names of dropped flavors
- Add names of new flavors

---

## Step 6 — Icon Processing

### New flavor icons

Request the icon image files from the user via the folder picker (`mcp__cowork__request_cowork_directory`).

Once files are on disk, run the bundled script to process all new icons:

```bash
python3 /Users/alexrocha/bigg-chill-site/bigg-chill-menu-update/scripts/process_icons.py \
  --src "/path/to/source/folder" \
  --dst "/Users/alexrocha/bigg-chill-site/public/flavor-icons" \
  --map "campfire-delight:campfire delight.png,dark-chocolate:Dark chocolate.png"
```

The script resizes to 384×384, removes the white background, saves as transparent RGBA WebP, and verifies each output.

**After processing, verify each icon:**
- Size: 384×384
- Mode: RGBA
- Corner pixel alpha ≈ 0 (transparent background)

### Removed flavor icons

Use `mcp__cowork__allow_cowork_file_delete` to request delete permission, then remove the icon files for dropped flavors from `public/flavor-icons/`. If the user rejects the delete prompt, list the exact filenames clearly so they can remove them manually.

---

## Step 7 — Pre-Publish Audit

Non-negotiable professional QA pass. Run every check programmatically. Report like a director of engineering signing off before a production deploy.

### Code integrity
- [ ] `currentFlavors` total count is correct
- [ ] Every `illustration` key in `currentFlavors` exists in `illustrationMap`
- [ ] No orphan keys in `illustrationMap` (defined but never used)
- [ ] Every `Dairy-Free` category flavor also appears in `dairyFreeFlavors`
- [ ] New flavors have correct categories, descriptions, and tags
- [ ] All allergen tag changes applied correctly
- [ ] No references to removed flavor names anywhere in source files
- [ ] No orphan illustration keys for removed flavors

### File system
- [ ] Every path in `illustrationMap` resolves to an actual file in `public/flavor-icons/`
- [ ] All new icon files are 384×384, RGBA, corner alpha = 0
- [ ] No dead icon files remain for removed flavors

### Sync
- [ ] `index.astro` ticker: removed flavors gone
- [ ] `index.astro` ticker: all new flavors present

### Sign-off format

Report each check as **✅ PASS** or **❌ FAIL — [details]**.

Fix any failure immediately and re-run that check before continuing.

Only after every check passes, deliver:

> **✅ All checks passed. The site is ready to publish.**
