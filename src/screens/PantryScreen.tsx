import { useMemo, useState } from "react"
import { FoodArt } from "../components/FoodArt.tsx"
import { GROUPS, STARTER, foodMap, pantry, pantryMap, recipes } from "../data/catalog.ts"
import type { AllergyId } from "../data/types.ts"
import { bestUnlock, planRecipe } from "../lib/match.ts"
import { formatNutrient } from "../lib/nutrition.ts"
import { UnlockCard } from "./RecipeScreens.tsx"

interface Props {
  selected: string[]
  allergies: AllergyId[]
  onToggle: (id: string) => void
  onSet: (ids: string[]) => void
  onOpen: (id: string) => void
  onShowRecipes: () => void
}

export function PantryScreen({ selected, allergies, onToggle, onSet, onOpen, onShowRecipes }: Props) {
  const [query, setQuery] = useState("")
  const chosen = useMemo(() => new Set(selected), [selected])
  const needle = query.trim().toLowerCase()
  const visible = useMemo(
    () => pantry.filter((item) => !needle || `${item.name} ${item.hint}`.toLowerCase().includes(needle)),
    [needle],
  )
  const planned = useMemo(
    () => recipes.map((recipe) => ({ recipe, plan: planRecipe(recipe, chosen, allergies, foodMap) })),
    [chosen, allergies],
  )
  const nowItems = planned.filter((item) => item.plan.fit === "now")
  const almostItems = planned.filter((item) => item.plan.fit === "almost")
  const matchCount = nowItems.length + almostItems.length
  const unlock = useMemo(
    () => (matchCount === 0 ? bestUnlock(chosen, allergies, foodMap, pantry, recipes) : null),
    [matchCount, chosen, allergies],
  )

  return (
    <div className={`grid gap-4 ${selected.length > 0 ? "pb-24" : ""}`}>
      <header>
        <h1 className="font-display text-4xl text-ink">What's in the kitchen?</h1>
        <p className="mt-1 text-lg font-bold text-ink/80">Tap every food you have. Big pictures, short names.</p>
      </header>
      <div className="flex flex-wrap gap-2">
        <button type="button" className="rounded-full bg-ink px-4 py-3 text-base font-extrabold text-white" onClick={() => onSet(STARTER)}>
          Tick a starter basket
        </button>
        <button type="button" className="rounded-full bg-white px-4 py-3 text-base font-extrabold text-ink" onClick={() => onSet([])}>
          Clear
        </button>
        <p className="self-center text-base font-extrabold text-ink">{selected.length} ticked</p>
      </div>
      <LiveMatches
        selectedCount={selected.length}
        nowItems={nowItems}
        almostItems={almostItems}
        unlock={unlock}
        onOpen={onOpen}
        onAdd={onToggle}
      />
      <label className="block">
        <span className="sr-only">Find a food</span>
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Find a food"
          className="w-full rounded-2xl border-2 border-ink/10 bg-white px-4 py-3 text-lg font-bold"
        />
      </label>
      {visible.length === 0 && <p className="rounded-3xl bg-white p-4 text-lg font-bold">No food matches that. Try “oats” or “yogurt”.</p>}
      {GROUPS.map((group) => {
        const items = visible.filter((item) => item.group === group)
        if (items.length === 0) return null
        return (
          <section key={group} className="grid gap-3">
            <h2 className="font-display text-2xl">{group}</h2>
            <ul className="grid grid-cols-2 gap-3 sm:grid-cols-3">
              {items.map((item) => {
                const on = chosen.has(item.id)
                return (
                  <li key={item.id}>
                    <button
                      type="button"
                      aria-pressed={on}
                      onClick={() => onToggle(item.id)}
                      className={`flex min-h-36 w-full flex-col items-center gap-2 rounded-3xl border-4 p-3 text-center ${on ? "border-leaf bg-white" : "border-transparent bg-white/80"}`}
                    >
                      <FoodArt id={item.id} className="h-20 w-20" />
                      <span className="text-lg font-extrabold leading-tight">{item.name}</span>
                      <span className="text-sm font-bold text-ink/60">{on ? "Got it" : item.hint}</span>
                    </button>
                  </li>
                )
              })}
            </ul>
          </section>
        )
      })}
      {selected.length > 0 && (
        <div className="fixed inset-x-0 bottom-[4.6rem] z-20 px-4">
          <button type="button" onClick={onShowRecipes} className="mx-auto block w-full max-w-5xl rounded-full bg-coral px-4 py-4 text-lg font-extrabold text-white shadow-lg">
            Show my recipes ({matchCount})
          </button>
        </div>
      )}
    </div>
  )
}

function LiveMatches({
  selectedCount,
  nowItems,
  almostItems,
  unlock,
  onOpen,
  onAdd,
}: {
  selectedCount: number
  nowItems: { recipe: { id: string; title: string }; plan: { perServing: { protein: number; fiber: number }; missing: string[] } }[]
  almostItems: { recipe: { id: string; title: string }; plan: { perServing: { protein: number; fiber: number }; missing: string[] } }[]
  unlock: { id: string; name: string; count: number } | null
  onOpen: (id: string) => void
  onAdd: (id: string) => void
}) {
  if (selectedCount === 0) {
    return (
      <section className="grid gap-3 rounded-[2rem] bg-white p-4">
        <h2 className="font-display text-2xl">Snacks show up here</h2>
        <p className="text-lg font-bold">Tap any food you have. The list changes right away.</p>
        <UnlockCard unlock={unlock} onAdd={onAdd} />
      </section>
    )
  }
  if (nowItems.length === 0 && almostItems.length === 0) {
    return (
      <section className="grid gap-3" aria-live="polite">
        <h2 className="font-display text-2xl">Nothing matches yet</h2>
        <UnlockCard unlock={unlock} onAdd={onAdd} />
      </section>
    )
  }
  return (
    <section className="grid gap-4" aria-live="polite">
      {nowItems.length > 0 && (
        <div className="grid gap-2">
          <h2 className="font-display text-2xl">You can bake now</h2>
          <ul className="grid gap-2">
            {nowItems.slice(0, 4).map((item) => (
              <LiveRow key={item.recipe.id} item={item} onOpen={onOpen} />
            ))}
          </ul>
          {nowItems.length > 4 && <p className="font-extrabold">{nowItems.length - 4} more {nowItems.length - 4 === 1 ? "is" : "are"} ready. The button below shows them all.</p>}
        </div>
      )}
      {almostItems.length > 0 && (
        <div className="grid gap-2">
          <h2 className="font-display text-2xl">Missing 1–2 ingredients</h2>
          <ul className="grid gap-2">
            {almostItems.slice(0, 4).map((item) => (
              <LiveRow key={item.recipe.id} item={item} onOpen={onOpen} />
            ))}
          </ul>
          {almostItems.length > 4 && <p className="font-extrabold">{almostItems.length - 4} more {almostItems.length - 4 === 1 ? "is" : "are"} close. The button below shows them all.</p>}
        </div>
      )}
    </section>
  )
}

function LiveRow({
  item,
  onOpen,
}: {
  item: { recipe: { id: string; title: string }; plan: { perServing: { protein: number; fiber: number }; missing: string[] } }
  onOpen: (id: string) => void
}) {
  return (
    <li>
      <button type="button" onClick={() => onOpen(item.recipe.id)} className="grid w-full gap-2 rounded-3xl bg-white p-3 text-left">
        <span className="font-display text-xl leading-tight">{item.recipe.title}</span>
        <span className="font-extrabold">
          {formatNutrient(item.plan.perServing.protein)} g protein · {formatNutrient(item.plan.perServing.fiber)} g fiber
        </span>
        {item.plan.missing.length > 0 && (
          <span className="flex flex-wrap gap-2">
            {item.plan.missing.map((id) => (
              <span key={id} className="flex items-center gap-1 rounded-full bg-blush pr-3">
                <FoodArt id={id} className="h-8 w-8" />
                <span className="font-extrabold">Need {pantryMap.get(id)?.name ?? id}</span>
              </span>
            ))}
          </span>
        )}
      </button>
    </li>
  )
}
