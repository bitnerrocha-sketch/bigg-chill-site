/**
 * Single source of truth for site-wide values.
 * Update these when contact info, hours, or the production domain changes.
 */

export const siteConfig = {
  name: "The Bigg Chill",
  tagline: "Handcrafted Ice Cream in Cody, Wyoming",
  description:
    "The Bigg Chill serves handcrafted small-batch ice cream in Cody, Wyoming with rotating flavors, gift cards, catering, and a love for the local community.",

  // Update to the production domain before public launch.
  // Also mirror this in astro.config.mjs (`site:`), public/robots.txt, and public/sitemap.xml.
  siteUrl: "https://thebiggchillicecream.netlify.app",

  business: {
    legalName: "The Bigg Chill Ice Cream",
    streetAddress: "1321 Sheridan Ave",
    city: "Cody",
    state: "Wyoming",
    stateShort: "WY",
    postalCode: "82414",
    country: "US",
    phone: "+13072507164",
    phoneDisplay: "(307) 250-7164",
    email: "biggchillmanagment@gmail.com",
  },

  hours: {
    schedules: [
      {
        days: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"] as const,
        opens: "12:00",
        closes: "22:00",
        display: "12–10 PM",
      },
    ],
  },

  social: {
    instagram: "https://www.instagram.com/the.bigg.chill/",
    facebook: "https://www.facebook.com/The.Bigg.Chill307/",
  },

  giftCardUrl: "https://app.squareup.com/gift/MLQY19DJP25AS/order",
  directionsUrl:
    "https://www.google.com/maps/search/?api=1&query=The%20Bigg%20Chill%20Cody%20WY",

  logo: "/logo-transparent.webp",
  brandImage: "/shop-front.webp",
  ogImage: "/og-image.webp",
  themeColor: "#ea605f",
} as const;

export type SiteConfig = typeof siteConfig;

/** Absolute URL for a given path. */
export function absoluteUrl(path: string): string {
  if (path.startsWith("http")) return path;
  return siteConfig.siteUrl.replace(/\/$/, "") + (path.startsWith("/") ? path : `/${path}`);
}
