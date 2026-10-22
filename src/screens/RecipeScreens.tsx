import { useEffect, useMemo, useState } from "react"
import { FoodArt } from "../components/FoodArt.tsx"
import { GrownupBadges, NutrientHero } from "../components/Meters.tsx"
import { STICKERS, foodMap, pantryMap, recipes } from "../data/catalog.ts"
import type { AllergyId, Recipe } from "../data/types.ts"
import { planRecipe, type Fit, type Plan } from "../lib/match.ts"
import { formatGrams, formatNutrient } from "../lib/nutrition.ts"

interface ListProps {
  pantry: string[]
  allergies: AllergyId[]
  favorites: string[]
  onOpen: (id: string) => void
  onFavorite: (id: string) => void
}

const TABS: { id: Fit | "all"; label: string }[] = [
  { id: "now", label: "Make now" },
  { id: "almost", label: "Almost" },
  { id: "all", label: "All snacks" },
]

export function RecipeList({ pantry, allergies, favorites, onOpen, onFavorite }: ListProps) {
  const [tab, setTab] = useState<(typeof TABS)[number]["id"]>("now")
  const [sort, setSort] = useState("protein")
  const [category, setCategory] = useState("All")
  const [powerOnly, setPowerOnly] = useState(false)
  const [query, setQuery] = useState("")
  const owned = useMemo(() => new Set(pantry), [pantry])
  const planned = useMemo(
    () => recipes.map((recipe) => ({ recipe, plan: planRecipe(recipe, owned, allergies, foodMap) })),
    [owned, allergies],
  )
  const categories = ["All", ...new Set(recipes.map((recipe) => recipe.category))]
  const counts = {
    now: planned.filter((item) => item.plan.fit === "now").length,
    almost: planned.filter((item) => item.plan.fit === "almost").length,
  }
  const needle = query.trim().toLowerCase()
  const shown = planned
    .filter((item) => item.plan.fit !== "hidden")
    .filter((item) => (tab === "all" ? true : item.plan.fit === tab))
    .filter((item) => category === "All" || item.recipe.category === category)
    .filter((item) => !powerOnly || item.plan.perServing.protein >= 8)
    .filter((item) => !needle || item.recipe.title.toLowerCase().includes(needle))
    .sort((a, b) => compare(a, b, sort))

  return (
    <div className="grid gap-4">
      <header>
        <h1 className="font-display text-4xl">Snacks we can make</h1>
        <p className="mt-1 text-lg font-bold text-ink/80">
          {counts.now} ready now · {counts.almost} almost there
        </p>
      </header>
      {pantry.length === 0 && (
        <p className="rounded-3xl bg-sun p-4 text-lg font-extrabold">
          The pantry is empty, so nothing is “ready now.” Tick foods you have, or browse All snacks.
        </p>
      )}
      <div className="flex gap-2 overflow-x-auto" role="tablist" aria-label="Which snacks">
        {TABS.map((item) => (
          <button
            key={item.id}
            type="button"
            role="tab"
            aria-selected={tab === item.id}
            onClick={() => setTab(item.id)}
            className={`shrink-0 rounded-full px-4 py-3 text-base font-extrabold ${tab === item.id ? "bg-ink text-white" : "bg-white text-ink"}`}
          >
            {item.label}
          </button>
        ))}
      </div>
      <div className="grid gap-3 sm:grid-cols-2">
        <label className="grid gap-1 text-sm font-extrabold">
          Sort
          <select value={sort} onChange={(event) => setSort(event.target.value)} className="rounded-2xl bg-white px-3 py-3 text-base">
            <option value="protein">Highest protein</option>
            <option value="fiber">Highest fiber</option>
            <option value="sugar">Lowest sugar</option>
            <option value="time">Shortest time</option>
            <option value="name">A to Z</option>
          </select>
        </label>
        <label className="grid gap-1 text-sm font-extrabold">
          Search
          <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Brownies, bark, bagels" className="rounded-2xl bg-white px-3 py-3 text-base font-bold" />
        </label>
      </div>
      <div className="flex gap-2 overflow-x-auto">
        {categories.map((item) => (
          <button key={item} type="button" onClick={() => setCategory(item)} className={`shrink-0 rounded-full px-3 py-2 text-sm font-extrabold ${category === item ? "bg-berry text-white" : "bg-white"}`}>
            {item}
          </button>
        ))}
        <button type="button" aria-pressed={powerOnly} onClick={() => setPowerOnly((value) => !value)} className={`shrink-0 rounded-full px-3 py-2 text-sm font-extrabold ${powerOnly ? "bg-coral text-white" : "bg-white"}`}>
          8 g protein or more
        </button>
      </div>
      {shown.length === 0 && (
        <p className="rounded-3xl bg-white p-4 text-lg font-bold">
          Nothing in this pile. Try All snacks, or turn off a filter. Safety switches hide recipes that are not safe.
        </p>
      )}
      <ul className="grid gap-3 md:grid-cols-2">
        {shown.map(({ recipe, plan }) => (
          <li key={recipe.id}>
            <article className="grid gap-3 rounded-3xl bg-white p-4 shadow-sm">
              <div className="flex items-start justify-between gap-3">
                <button type="button" onClick={() => onOpen(recipe.id)} className="text-left">
                  <p className="text-sm font-extrabold uppercase tracking-wide text-berry">{recipe.category}</p>
                  <h2 className="font-display text-2xl leading-tight">{recipe.title}</h2>
                </button>
                <button type="button" aria-pressed={favorites.includes(recipe.id)} aria-label={favorites.includes(recipe.id) ? "Remove favorite" : "Save favorite"} onClick={() => onFavorite(recipe.id)} className="rounded-full bg-blush px-3 py-2 text-xl">
                  {favorites.includes(recipe.id) ? "♥" : "♡"}
                </button>
              </div>
              <button type="button" onClick={() => onOpen(recipe.id)} className="grid grid-cols-2 gap-2 text-left">
                <Stat label="Protein" value={`${formatNutrient(plan.perServing.protein)} g`} />
                <Stat label="Fiber" value={`${formatNutrient(plan.perServing.fiber)} g`} />
              </button>
              <FitLine plan={plan} />
              <button type="button" onClick={() => onOpen(recipe.id)} className="rounded-full bg-coral px-4 py-3 text-base font-extrabold text-white">
                Open this snack
              </button>
            </article>
          </li>
        ))}
      </ul>
    </div>
  )
}

function compare(a: { recipe: Recipe; plan: Plan }, b: { recipe: Recipe; plan: Plan }, sort: string) {
  if (sort === "fiber") return b.plan.perServing.fiber - a.plan.perServing.fiber
  if (sort === "sugar") return a.plan.perServing.sugar - b.plan.perServing.sugar
  if (sort === "time") return a.recipe.minutes - b.recipe.minutes
  if (sort === "name") return a.recipe.title.localeCompare(b.recipe.title)
  return b.plan.perServing.protein - a.plan.perServing.protein
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl bg-cream px-3 py-2">
      <p className="text-xs font-extrabold uppercase text-ink/50">{label}</p>
      <p className="font-display text-3xl">{value}</p>
    </div>
  )
}

function FitLine({ plan }: { plan: Plan }) {
  if (plan.fit === "now" && plan.swaps.length === 0) {
    return <p className="rounded-2xl bg-leaf/10 px-3 py-2 font-extrabold text-leaf">You can make this now.</p>
  }
  if (plan.fit === "now") {
    return (
      <div className="rounded-2xl bg-leaf/10 px-3 py-2 font-extrabold text-leaf">
        <p>You can make this with a swap.</p>
        {plan.swaps.map((swap) => (
          <p key={swap.id} className="mt-1 text-sm text-ink">{swap.label}</p>
        ))}
      </div>
    )
  }
  return (
    <div className="grid gap-2">
      <p className="font-extrabold">{plan.fit === "almost" ? "Almost there. Still need:" : "Needs more foods:"}</p>
      {plan.swaps.map((swap) => (
        <p key={swap.id} className="text-sm font-bold text-ink/80">{swap.label}</p>
      ))}
      <ul className="flex flex-wrap gap-2">
        {plan.missing.map((id) => (
          <li key={id} className="flex items-center gap-2 rounded-full bg-blush pr-3">
            <FoodArt id={id} className="h-10 w-10" />
            <span className="font-extrabold">{pantryMap.get(id)?.name ?? id}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}

interface DetailProps {
  id: string
  pantry: string[]
  allergies: AllergyId[]
  favorite: boolean
  onBack: () => void
  onFavorite: () => void
  onKid: () => void
  onMade: (sticker: string) => void
}

export function RecipeDetail({ id, pantry, allergies, favorite, onBack, onFavorite, onKid, onMade }: DetailProps) {
  const recipe = recipes.find((item) => item.id === id)
  const [picking, setPicking] = useState(false)
  const [savedSticker, setSavedSticker] = useState<string | null>(null)
  if (!recipe) return <p className="text-lg font-bold">That snack is missing.</p>
  const plan = planRecipe(recipe, new Set(pantry), allergies, foodMap)
  return (
    <div className="grid gap-4">
      <button type="button" onClick={onBack} className="w-fit rounded-full bg-white px-4 py-2 font-extrabold">
        Back to snacks
      </button>
      <header className="grid gap-2">
        <p className="font-extrabold uppercase tracking-wide text-berry">{recipe.category}</p>
        <div className="flex items-start justify-between gap-3">
          <h1 className="font-display text-4xl leading-tight">{recipe.title}</h1>
          <button type="button" aria-pressed={favorite} aria-label={favorite ? "Remove favorite" : "Save favorite"} onClick={onFavorite} className="rounded-full bg-white px-3 py-2 text-2xl">
            {favorite ? "♥" : "♡"}
          </button>
        </div>
        <p className="text-lg font-bold">{recipe.blurb}</p>
        <p className="text-base font-bold text-ink/70">
          About {recipe.minutes} minutes · makes {recipe.servings} · one serving is {recipe.servingLabel}
        </p>
        <a className="font-extrabold text-sky underline" href={recipe.sourceUrl} target="_blank" rel="noreferrer">
          Recipe from {recipe.sourceName} — {recipe.author}
        </a>
      </header>
      <NutrientHero nutrients={plan.perServing} servingLabel={recipe.servingLabel} />
      {plan.swaps.length > 0 && (
        <section className="rounded-3xl bg-sun p-4">
          <h2 className="font-display text-2xl">Swap to make it</h2>
          <ul className="mt-2 grid gap-2">
            {plan.swaps.map((swap) => (
              <li key={swap.id}>
                <p className="font-extrabold">{swap.label}</p>
                <p className="text-sm font-bold">{swap.source}</p>
              </li>
            ))}
          </ul>
        </section>
      )}
      {plan.fit !== "now" && <FitLine plan={plan} />}
      {recipe.swaps.length > 0 && plan.swaps.length === 0 && (
        <section className="rounded-3xl bg-white p-4">
          <h2 className="font-display text-2xl">Swaps if you are missing something</h2>
          <ul className="mt-2 grid gap-2">
            {recipe.swaps.map((swap) => (
              <li key={swap.id} className="rounded-2xl bg-cream p-3">
                <p className="font-extrabold">{swap.label}</p>
                <p className="text-sm font-bold text-ink/70">{swap.source}</p>
              </li>
            ))}
          </ul>
        </section>
      )}
      <section className="grid gap-2">
        <h2 className="font-display text-2xl">Ingredients</h2>
        <ul className="grid gap-2">
          {recipe.lines.map((line, index) => {
            const have = pantry.includes(line.pantryId)
            return (
              <li key={`${line.foodId}-${index}`} className="flex items-center gap-3 rounded-3xl bg-white p-2">
                <FoodArt id={line.pantryId} className="h-16 w-16 shrink-0" />
                <div>
                  <p className="text-lg font-extrabold">{line.amount}</p>
                  <p className="text-sm font-bold text-ink/60">{have ? "You have this" : `Need ${pantryMap.get(line.pantryId)?.name}`}</p>
                </div>
              </li>
            )
          })}
        </ul>
      </section>
      <MathPanel recipe={recipe} plan={plan} />
      <button type="button" onClick={onKid} className="rounded-full bg-ink px-4 py-4 text-xl font-extrabold text-white">
        Start kid mode
      </button>
      <button type="button" onClick={() => setPicking(true)} className="rounded-full bg-berry px-4 py-4 text-xl font-extrabold text-white">
        I made it!
      </button>
      {picking && (
        <section className="rounded-3xl bg-white p-4">
          <h2 className="font-display text-2xl">Pick a sticker</h2>
          <ul className="mt-3 grid grid-cols-3 gap-2">
            {STICKERS.map((sticker) => (
              <li key={sticker.id}>
                <button
                  type="button"
                  className="flex w-full flex-col items-center rounded-3xl bg-cream px-2 py-3"
                  onClick={() => {
                    onMade(sticker.id)
                    setSavedSticker(sticker.label)
                    setPicking(false)
                  }}
                >
                  <span className="text-4xl" aria-hidden="true">{sticker.glyph}</span>
                  <span className="font-extrabold">{sticker.label}</span>
                </button>
              </li>
            ))}
          </ul>
        </section>
      )}
      {savedSticker && <p className="rounded-3xl bg-leaf/15 p-4 text-lg font-extrabold text-leaf" role="status">{savedSticker} is in your sticker book.</p>}
    </div>
  )
}

function MathPanel({ recipe, plan }: { recipe: Recipe; plan: Plan }) {
  const batch = plan.math.reduce(
    (total, row) => {
      if (!row.amount) return total
      return {
        kcal: total.kcal + row.amount.kcal,
        protein: total.protein + row.amount.protein,
        fiber: total.fiber + row.amount.fiber,
        sugar: total.sugar + row.amount.sugar,
      }
    },
    { kcal: 0, protein: 0, fiber: 0, sugar: 0 },
  )
  return (
    <section className="grid gap-3 rounded-3xl bg-white p-4">
      <h2 className="font-display text-2xl">How we counted</h2>
      <p className="font-bold">
        Each gram weight is multiplied by the USDA amount per 100 grams. We add those up, then divide by {recipe.servings}. These are the raw ingredients, not a lab test of the baked snack.
        {plan.swaps.length > 0 ? " This count uses the swap above." : ""}
      </p>
      <ul className="grid gap-3">
        {plan.math.map((row, index) => (
          <li key={`${row.line.foodId}-${index}`} className="rounded-2xl bg-cream p-3">
            <p className="font-extrabold">
              {row.line.amount}
              {row.line.grams != null ? ` · ${formatGrams(row.line.grams)} g` : " · no gram weight"}
            </p>
            <p className="text-sm font-bold text-ink/70">{row.line.gramNote}</p>
            {row.food.fdcId && row.food.per100g ? (
              <>
                <p className="mt-1 text-sm font-bold">
                  <a className="underline" href={row.food.fdcUrl ?? undefined} target="_blank" rel="noreferrer">
                    FDC {row.food.fdcId}
                  </a>
                  {" · "}
                  {row.food.fdcName}
                </p>
                {row.amount && row.line.grams != null && (
                  <ul className="mt-1 text-sm font-bold">
                    <li>Protein {formatGrams(row.line.grams)} × {row.food.per100g.protein} ÷ 100 = {formatNutrient(row.amount.protein, 2)} g</li>
                    <li>Fiber {formatGrams(row.line.grams)} × {row.food.per100g.fiber} ÷ 100 = {formatNutrient(row.amount.fiber, 2)} g</li>
                    <li>Calories {formatGrams(row.line.grams)} × {row.food.per100g.kcal} ÷ 100 = {formatNutrient(row.amount.kcal, 1)} kcal</li>
                    <li>Sugar {formatGrams(row.line.grams)} × {row.food.per100g.sugar} ÷ 100 = {formatNutrient(row.amount.sugar, 2)} g</li>
                  </ul>
                )}
                {row.food.note && <p className="mt-1 text-sm font-bold text-ink/70">{row.food.note}</p>}
              </>
            ) : (
              <p className="mt-1 font-extrabold">Not in the USDA tables we used, so this line is not in the total.</p>
            )}
          </li>
        ))}
      </ul>
      {recipe.unquantified.map((note) => (
        <p key={note} className="rounded-2xl bg-blush p-3 text-sm font-bold">{note}</p>
      ))}
      <div className="rounded-2xl bg-ink p-4 text-white">
        <p className="font-extrabold">Whole batch</p>
        <p>Protein {formatNutrient(batch.protein, 2)} g · Fiber {formatNutrient(batch.fiber, 2)} g · {formatNutrient(batch.kcal, 0)} kcal · Sugar {formatNutrient(batch.sugar, 2)} g</p>
        <p className="mt-2 font-extrabold">Divide by {recipe.servings}</p>
        <p>
          Protein {formatNutrient(plan.perServing.protein)} g · Fiber {formatNutrient(plan.perServing.fiber)} g · {formatNutrient(plan.perServing.kcal, 0)} kcal · Sugar {formatNutrient(plan.perServing.sugar)} g per {recipe.servingLabel}
        </p>
      </div>
    </section>
  )
}

export function KidMode({
  id,
  quiet,
  onClose,
}: {
  id: string
  quiet: boolean
  onClose: () => void
}) {
  const recipe = recipes.find((item) => item.id === id)
  const [stepIndex, setStepIndex] = useState(0)
  if (!recipe) return <p>That snack is missing.</p>
  const step = recipe.steps[stepIndex]
  const last = stepIndex === recipe.steps.length - 1
  return (
    <div className="grid min-h-[70vh] gap-5">
      <div className="flex items-center justify-between gap-3">
        <button type="button" onClick={onClose} className="rounded-full bg-white px-4 py-2 font-extrabold">
          Close
        </button>
        <p className="font-extrabold">
          Step {stepIndex + 1} of {recipe.steps.length}
        </p>
      </div>
      <div className="flex gap-2" aria-hidden="true">
        {recipe.steps.map((item, index) => (
          <span key={item.text} className={`h-3 flex-1 rounded-full ${index <= stepIndex ? "bg-coral" : "bg-white"}`} />
        ))}
      </div>
      <h1 className="font-display text-3xl">{recipe.title}</h1>
      <GrownupBadges kinds={step.grownup} />
      <p className="font-display text-4xl leading-tight sm:text-5xl">{step.text}</p>
      {step.timerSec && step.timerLabel && <Timer key={stepIndex} seconds={step.timerSec} label={step.timerLabel} quiet={quiet} />}
      <div className="mt-auto grid grid-cols-2 gap-3">
        <button type="button" disabled={stepIndex === 0} onClick={() => setStepIndex((value) => value - 1)} className="rounded-full bg-white px-4 py-4 text-xl font-extrabold disabled:opacity-40">
          Back
        </button>
        {last ? (
          <button type="button" onClick={onClose} className="rounded-full bg-leaf px-4 py-4 text-xl font-extrabold text-white">
            Done
          </button>
        ) : (
          <button type="button" onClick={() => setStepIndex((value) => value + 1)} className="rounded-full bg-ink px-4 py-4 text-xl font-extrabold text-white">
            Next
          </button>
        )}
      </div>
    </div>
  )
}

function Timer({ seconds, label, quiet }: { seconds: number; label: string; quiet: boolean }) {
  const [left, setLeft] = useState<number | null>(null)
  useEffect(() => {
    if (left == null || left <= 0) return
    const id = window.setTimeout(() => setLeft(left - 1), 1000)
    return () => window.clearTimeout(id)
  }, [left])
  useEffect(() => {
    if (left === 0 && !quiet) beep()
  }, [left, quiet])
  const running = left != null && left > 0
  const done = left === 0
  return (
    <div className="rounded-3xl bg-white p-4">
      <p className="text-lg font-extrabold">Timer · {label}</p>
      <p className="font-display text-5xl" aria-live="polite">
        {left == null ? label : formatClock(left)}
      </p>
      {done && <p className="text-xl font-extrabold text-leaf">Time is up. Ask a grown-up to check.</p>}
      <button type="button" onClick={() => setLeft(running ? null : seconds)} className="mt-3 rounded-full bg-sun px-4 py-3 text-lg font-extrabold">
        {running ? "Stop timer" : done ? "Start again" : "Start timer"}
      </button>
    </div>
  )
}

function formatClock(total: number) {
  const minutes = Math.floor(total / 60)
  const seconds = total % 60
  return `${minutes}:${String(seconds).padStart(2, "0")}`
}

function beep() {
  const context = new AudioContext()
  const osc = context.createOscillator()
  const gain = context.createGain()
  osc.frequency.value = 880
  gain.gain.value = 0.05
  osc.connect(gain)
  gain.connect(context.destination)
  osc.start()
  osc.stop(context.currentTime + 0.25)
  osc.onended = () => void context.close()
}
