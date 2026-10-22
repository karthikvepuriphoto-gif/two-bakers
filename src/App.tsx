import { useMemo, useState } from "react"
import { FoodArt } from "./components/FoodArt.tsx"
import { ALLERGIES, STICKERS, foodMap, pantryMap, recipes } from "./data/catalog.ts"
import type { AllergyId } from "./data/types.ts"
import { planRecipe } from "./lib/match.ts"
import { useSaved } from "./lib/storage.ts"
import { PantryScreen } from "./screens/PantryScreen.tsx"
import { KidMode, RecipeDetail, RecipeList } from "./screens/RecipeScreens.tsx"

type Page =
  | { name: "home" }
  | { name: "pantry" }
  | { name: "recipes" }
  | { name: "recipe"; id: string }
  | { name: "kid"; id: string }
  | { name: "stickers" }
  | { name: "safety" }

export default function App() {
  const { saved, togglePantry, toggleAllergy, toggleFavorite, addMade, setQuiet, setPantry, clearMade } = useSaved()
  const [page, setPage] = useState<Page>({ name: "home" })
  const owned = useMemo(() => new Set(saved.pantry), [saved.pantry])
  const counts = useMemo(() => {
    let now = 0
    let almost = 0
    for (const recipe of recipes) {
      const fit = planRecipe(recipe, owned, saved.allergies, foodMap).fit
      if (fit === "now") now += 1
      if (fit === "almost") almost += 1
    }
    return { now, almost }
  }, [owned, saved.allergies])

  return (
    <div className="mx-auto min-h-screen max-w-5xl px-4 pb-28 pt-4">
      <a href="#main" className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-20 focus:rounded-full focus:bg-white focus:px-4 focus:py-2">
        Skip to the snack
      </a>
      <header className="mb-4 flex items-center justify-between gap-3">
        <button type="button" onClick={() => setPage({ name: "home" })} className="text-left">
          <p className="font-display text-3xl leading-none">Two Bakers</p>
          <p className="text-sm font-extrabold text-ink/70">Karthik's kitchen</p>
        </button>
        <button type="button" onClick={() => setPage({ name: "safety" })} className="rounded-full bg-white px-4 py-3 font-extrabold">
          Safety
        </button>
      </header>
      <main id="main">
        {page.name === "home" && (
          <Home
            now={counts.now}
            almost={counts.almost}
            made={saved.made.length}
            favorites={saved.favorites.length}
            onPantry={() => setPage({ name: "pantry" })}
            onRecipes={() => setPage({ name: "recipes" })}
            onStickers={() => setPage({ name: "stickers" })}
            onSafety={() => setPage({ name: "safety" })}
          />
        )}
        {page.name === "pantry" && <PantryScreen selected={saved.pantry} onToggle={togglePantry} onSet={setPantry} />}
        {page.name === "recipes" && (
          <RecipeList
            pantry={saved.pantry}
            allergies={saved.allergies}
            favorites={saved.favorites}
            onOpen={(id) => setPage({ name: "recipe", id })}
            onFavorite={toggleFavorite}
          />
        )}
        {page.name === "recipe" && (
          <RecipeDetail
            id={page.id}
            pantry={saved.pantry}
            allergies={saved.allergies}
            favorite={saved.favorites.includes(page.id)}
            onBack={() => setPage({ name: "recipes" })}
            onFavorite={() => toggleFavorite(page.id)}
            onKid={() => setPage({ name: "kid", id: page.id })}
            onMade={(sticker) => addMade({ id: crypto.randomUUID(), recipeId: page.id, sticker, at: Date.now() })}
          />
        )}
        {page.name === "kid" && <KidMode id={page.id} quiet={saved.quiet} onClose={() => setPage({ name: "recipe", id: page.id })} />}
        {page.name === "stickers" && (
          <StickerBook
            made={saved.made}
            onOpen={(id) => setPage({ name: "recipe", id })}
          />
        )}
        {page.name === "safety" && (
          <Safety
            allergies={saved.allergies}
            quiet={saved.quiet}
            onAllergy={toggleAllergy}
            onQuiet={setQuiet}
            onClearPantry={() => setPantry([])}
            onClearMade={clearMade}
          />
        )}
      </main>
      <nav className="fixed inset-x-0 bottom-0 z-10 border-t border-ink/10 bg-cream/95 px-4 py-2 backdrop-blur" aria-label="Main">
        <ul className="mx-auto grid max-w-5xl grid-cols-4 gap-2">
          <NavButton label="Home" current={page.name === "home"} onClick={() => setPage({ name: "home" })} />
          <NavButton label="Pantry" current={page.name === "pantry"} onClick={() => setPage({ name: "pantry" })} />
          <NavButton label="Snacks" current={page.name === "recipes" || page.name === "recipe" || page.name === "kid"} onClick={() => setPage({ name: "recipes" })} />
          <NavButton label="Stickers" current={page.name === "stickers"} onClick={() => setPage({ name: "stickers" })} />
        </ul>
      </nav>
    </div>
  )
}

function NavButton({ label, current, onClick }: { label: string; current: boolean; onClick: () => void }) {
  return (
    <li>
      <button type="button" aria-current={current ? "page" : undefined} onClick={onClick} className={`w-full rounded-2xl px-2 py-3 text-base font-extrabold ${current ? "bg-ink text-white" : "bg-white"}`}>
        {label}
      </button>
    </li>
  )
}

function Home({
  now,
  almost,
  made,
  favorites,
  onPantry,
  onRecipes,
  onStickers,
  onSafety,
}: {
  now: number
  almost: number
  made: number
  favorites: number
  onPantry: () => void
  onRecipes: () => void
  onStickers: () => void
  onSafety: () => void
}) {
  return (
    <div className="grid gap-4">
      <section className="rounded-[2rem] bg-white p-5 shadow-sm">
        <div className="flex items-end justify-between gap-3">
          <div>
            <p className="font-extrabold uppercase tracking-wide text-coral">For a daughter and a son</p>
            <h1 className="font-display text-5xl leading-none">Hi, bakers.</h1>
          </div>
          <div className="flex gap-1">
            <FoodArt id="banana" className="h-16 w-16" />
            <FoodArt id="egg" className="h-16 w-16" />
          </div>
        </div>
        <p className="mt-3 text-lg font-bold">
          Pip the banana and Dot the egg help Karthik's kids find a snack from foods already in the kitchen.
        </p>
      </section>
      <div className="grid gap-3 sm:grid-cols-2">
        <button type="button" onClick={onPantry} className="rounded-[2rem] bg-sun p-5 text-left">
          <p className="font-display text-3xl">Tick the pantry</p>
          <p className="mt-1 text-lg font-bold">Pictures of bananas, oats, yogurt, and the rest.</p>
        </button>
        <button type="button" onClick={onRecipes} className="rounded-[2rem] bg-coral p-5 text-left text-white">
          <p className="font-display text-3xl">{now} ready now</p>
          <p className="mt-1 text-lg font-extrabold">{almost} more are one or two foods away.</p>
        </button>
      </div>
      <div className="grid grid-cols-2 gap-3">
        <button type="button" onClick={onStickers} className="rounded-3xl bg-white p-4 text-left">
          <p className="font-display text-3xl">{made}</p>
          <p className="font-extrabold">stickers earned</p>
        </button>
        <button type="button" onClick={onRecipes} className="rounded-3xl bg-white p-4 text-left">
          <p className="font-display text-3xl">{favorites}</p>
          <p className="font-extrabold">favorites saved</p>
        </button>
      </div>
      <button type="button" onClick={onSafety} className="rounded-3xl bg-white p-4 text-left">
        <p className="font-display text-2xl">Grown-up safety switches</p>
        <p className="font-bold">Hide peanut, dairy, egg, or gluten recipes. This phone remembers your ticks.</p>
      </button>
      <p className="text-sm font-bold text-ink/70">
        Recipes come from the cooks we link. Protein, fiber, calories, and sugar are counted from USDA FoodData Central, not copied from the recipe page.
      </p>
    </div>
  )
}

function StickerBook({ made, onOpen }: { made: { id: string; recipeId: string; sticker: string; at: number }[]; onOpen: (id: string) => void }) {
  if (made.length === 0) {
    return (
      <div className="grid gap-3">
        <h1 className="font-display text-4xl">Sticker book</h1>
        <p className="rounded-3xl bg-white p-4 text-lg font-bold">No stickers yet. Make a snack, then tap “I made it!” and pick one.</p>
      </div>
    )
  }
  return (
    <div className="grid gap-4">
      <h1 className="font-display text-4xl">Sticker book</h1>
      <ul className="grid grid-cols-2 gap-3 sm:grid-cols-3">
        {made.map((stamp) => {
          const sticker = STICKERS.find((item) => item.id === stamp.sticker)
          const recipe = recipes.find((item) => item.id === stamp.recipeId)
          return (
            <li key={stamp.id}>
              <button type="button" onClick={() => recipe && onOpen(recipe.id)} className="flex h-full w-full flex-col items-center gap-2 rounded-3xl bg-white p-4 text-center">
                <span className="text-5xl" aria-hidden="true">{sticker?.glyph}</span>
                <span className="font-extrabold">{sticker?.label}</span>
                <span className="text-sm font-bold">{recipe?.title ?? "A snack"}</span>
                <span className="text-xs font-bold text-ink/60">{new Date(stamp.at).toLocaleDateString()}</span>
              </button>
            </li>
          )
        })}
      </ul>
    </div>
  )
}

function Safety({
  allergies,
  quiet,
  onAllergy,
  onQuiet,
  onClearPantry,
  onClearMade,
}: {
  allergies: AllergyId[]
  quiet: boolean
  onAllergy: (id: AllergyId) => void
  onQuiet: (value: boolean) => void
  onClearPantry: () => void
  onClearMade: () => void
}) {
  return (
    <div className="grid gap-4">
      <header>
        <h1 className="font-display text-4xl">Safety switches</h1>
        <p className="mt-1 text-lg font-bold">A grown-up sets these. The phone keeps them. They are not a doctor’s note.</p>
      </header>
      <ul className="grid gap-3">
        {ALLERGIES.map((item) => {
          const on = allergies.includes(item.id)
          return (
            <li key={item.id}>
              <button type="button" role="switch" aria-checked={on} onClick={() => onAllergy(item.id)} className="flex w-full items-center justify-between gap-3 rounded-3xl bg-white p-4 text-left">
                <span>
                  <span className="block font-display text-2xl">{item.label}</span>
                  <span className="block font-bold text-ink/70">{item.detail}</span>
                </span>
                <span className={`rounded-full px-3 py-2 font-extrabold ${on ? "bg-coral text-white" : "bg-cream"}`}>{on ? "Hiding" : "Off"}</span>
              </button>
            </li>
          )
        })}
      </ul>
      <button type="button" role="switch" aria-checked={quiet} onClick={() => onQuiet(!quiet)} className="flex items-center justify-between rounded-3xl bg-white p-4 text-left">
        <span>
          <span className="block font-display text-2xl">Quiet timers</span>
          <span className="block font-bold text-ink/70">No beep when a timer ends.</span>
        </span>
        <span className={`rounded-full px-3 py-2 font-extrabold ${quiet ? "bg-ink text-white" : "bg-cream"}`}>{quiet ? "Quiet" : "Beep"}</span>
      </button>
      <section className="rounded-3xl bg-white p-4">
        <h2 className="font-display text-2xl">What the numbers mean</h2>
        <p className="mt-2 font-bold">
          Protein, fiber, calories, and sugar are counted from USDA FoodData Central, SR Legacy, April 2018. We use the gram weight of each ingredient, multiply by the USDA amount per 100 grams, add them up, and divide by the servings. Baking can change weight as water leaves, so this is the ingredient tally, not a lab test.
        </p>
        <p className="mt-2 font-bold">Chocolate chips are treated as dairy. Oats are treated as a gluten risk unless a grown-up knows the oats are certified gluten-free. Rice paper has no USDA record here, so those sheets are left out of the bagel numbers.</p>
      </section>
      <div className="grid gap-2 sm:grid-cols-2">
        <button type="button" onClick={onClearPantry} className="rounded-full bg-white px-4 py-3 font-extrabold">Clear the pantry ticks</button>
        <button type="button" onClick={onClearMade} className="rounded-full bg-white px-4 py-3 font-extrabold">Clear the sticker book</button>
      </div>
      <p className="text-sm font-bold text-ink/60">Pantry names on this phone: {pantryMap.size}. Recipes saved in the app: {recipes.length}.</p>
    </div>
  )
}
