# Two Bakers

A mobile-first snack app for Karthik Vepuri’s daughter and son. Kids tick the foods they have. The app shows recipes they can make now, and recipes that are one or two ingredients away.

It is a static installable web app. Nothing is stored on a server. Pantry ticks, allergy switches, favorites, and the “I made it” sticker book stay in the browser on the device.

## Run it

```bash
npm install
npm run dev -- --host 0.0.0.0 --port 43123
```

Open http://127.0.0.1:43123/two-bakers/

The Vite `base` is `/two-bakers/`, the same path GitHub Pages uses.

To build the files a static host serves:

```bash
npm run build
npm run preview -- --host 0.0.0.0 --port 43123
```

Open the preview at http://127.0.0.1:43123/two-bakers/

The built site is in `dist/`, including a web app manifest and a service worker so a phone can install it. Manifest `start_url` and `scope`, and the service worker, are `/two-bakers/`.

## Where the recipes and numbers come from

Every recipe is a published one. The snack page links to the cook. Steps are shortened for a young reader. Temperatures, times, and ingredient amounts follow the source.

Protein, fiber, calories, and sugar are not copied from those pages. They are counted from [USDA FoodData Central SR Legacy (April 2018)](https://fdc.nal.usda.gov/):

1. Turn the written amount into grams, using the author’s gram weight when they printed one, otherwise the USDA household portion.
2. Multiply grams by that food’s USDA amount per 100 grams.
3. Add the ingredients.
4. Divide by the number of servings.

Open **How we counted** on any snack to see the FDC id, the gram weight, and the multiplication. A few foods are called out when USDA has no exact match (rice paper wrappers, oat flour by the cup, Greek yogurt by the cup, flavored protein powder).

Allergy switches hide peanut, dairy, egg, and gluten recipes. Oats count as a gluten risk. Chocolate chips count as dairy. A written swap does not bring a hidden recipe back, because the steps still name the original food. Yogurt in place of an egg is only offered when eggs are allowed and the egg is simply missing.

## GitHub Pages

The public site is https://karthikvepuriphoto-gif.github.io/two-bakers/

Source lives at https://github.com/karthikvepuriphoto-gif/two-bakers

`.github/workflows/pages.yml` runs `npm ci` and `npm run build` on every push to `main`, then deploys `dist` with GitHub Pages. In the repository settings, Pages source must be GitHub Actions.

On a phone, open the Pages URL in Chrome or Safari and use **Add to Home Screen** or the install prompt. The service worker caches the app for offline use after the first visit.
