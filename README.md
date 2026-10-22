# Two Bakers

A mobile-first snack app for Karthik Vepuri’s daughter and son. Kids tick the foods they have. The app shows recipes they can make now, and recipes that are one or two ingredients away.

It is a static installable web app. Nothing is stored on a server. Pantry ticks, allergy switches, favorites, and the “I made it” sticker book stay in the browser on the device.

## Run it

```bash
npm install
npm run dev -- --host 0.0.0.0 --port 43123
```

Open http://127.0.0.1:43123

To build the files a static host serves:

```bash
npm run build
npm run preview -- --host 0.0.0.0 --port 43123
```

The built site is in `dist/`, including a web app manifest and a service worker so a phone can install it.

## Where the recipes and numbers come from

Every recipe is a published one. The snack page links to the cook. Steps are shortened for a young reader. Temperatures, times, and ingredient amounts follow the source.

Protein, fiber, calories, and sugar are not copied from those pages. They are counted from [USDA FoodData Central SR Legacy (April 2018)](https://fdc.nal.usda.gov/):

1. Turn the written amount into grams, using the author’s gram weight when they printed one, otherwise the USDA household portion.
2. Multiply grams by that food’s USDA amount per 100 grams.
3. Add the ingredients.
4. Divide by the number of servings.

Open **How we counted** on any snack to see the FDC id, the gram weight, and the multiplication. A few foods are called out when USDA has no exact match (rice paper wrappers, oat flour by the cup, Greek yogurt by the cup, flavored protein powder).

Allergy switches hide peanut, dairy, egg, and gluten recipes. Oats count as a gluten risk. Chocolate chips count as dairy. A written swap does not bring a hidden recipe back, because the steps still name the original food. Yogurt in place of an egg is only offered when eggs are allowed and the egg is simply missing.

## Move it to GitHub Pages later

The app is a single-page static build.

1. Create a GitHub repository and push this project.
2. If the site will live at `https://USERNAME.github.io/REPO/`, set the Vite base in `vite.config.ts`:

```ts
export default defineConfig({
  base: "/REPO/",
  // ...plugins
})
```

Leave `base` as `"/"` for a user site at `https://USERNAME.github.io/` or for any host that serves the site at the domain root.

3. Build:

```bash
npm run build
```

4. Deploy the `dist` folder. With the `gh-pages` package:

```bash
npx gh-pages -d dist
```

Or in the repository settings, use GitHub Actions to run `npm ci`, `npm run build`, and upload `dist` to the Pages environment. Set the Pages source to GitHub Actions.

5. On a phone, open the Pages URL in Chrome or Safari and use **Add to Home Screen** or the install prompt. The service worker caches the app for offline use after the first visit.
