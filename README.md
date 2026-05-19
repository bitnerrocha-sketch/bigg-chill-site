# The Bigg Chill — Website

Handcrafted small-batch ice cream in Cody, Wyoming. Astro site, three pages: `/`, `/menu`, `/catering`.

## Local development

```sh
npm install
npm run dev      # http://localhost:4321
```

## Build

```sh
npm run build    # outputs to ./dist/
npm run preview  # serves the build locally
```

## Project structure

- `src/pages/` — one file per route.
- `src/lib/siteConfig.ts` — **single source of truth** for site URL, business info (NAP), hours, social links, and the gift-card URL. Update this when contact info, hours, or the production domain changes.
- `public/` — static assets served as-is: `robots.txt`, `sitemap.xml`, `manifest.webmanifest`, favicons, images.

## Before public launch

1. Set the production domain in **three places** (keep them in sync):
   - `src/lib/siteConfig.ts` → `siteUrl`
   - `astro.config.mjs` → `site`
   - `public/robots.txt` and `public/sitemap.xml`
2. Replace `public/shop-front.webp` (currently used as the social-share image) with a branded 1200×630 OG image, or point `siteConfig.ogImage` at one.
3. Run a Lighthouse pass; address remaining items from `AUDIT.md`.

## Hosting

Deploys to Netlify. The catering quote form uses Netlify Forms (`data-netlify="true"`).
