import { useMemo, useState } from "react"
import { FoodArt } from "../components/FoodArt.tsx"
import { GROUPS, STARTER, pantry } from "../data/catalog.ts"

interface Props {
  selected: string[]
  onToggle: (id: string) => void
  onSet: (ids: string[]) => void
}

export function PantryScreen({ selected, onToggle, onSet }: Props) {
  const [query, setQuery] = useState("")
  const chosen = new Set(selected)
  const needle = query.trim().toLowerCase()
  const visible = useMemo(
    () => pantry.filter((item) => !needle || `${item.name} ${item.hint}`.toLowerCase().includes(needle)),
    [needle],
  )

  return (
    <div className="grid gap-4">
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
    </div>
  )
}
