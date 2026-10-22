import type { AllergyId, Food, Recipe, RecipeLine, Swap } from "../data/types.ts"
import { lineMath, perServing, sumLines, type LineMath } from "./nutrition.ts"

export type Fit = "now" | "almost" | "later" | "hidden"

export interface Plan {
  fit: Fit
  missing: string[]
  swaps: Swap[]
  lines: RecipeLine[]
  math: LineMath[]
  perServing: ReturnType<typeof perServing>
}

function combos(swaps: Swap[]): Swap[][] {
  let out: Swap[][] = [[]]
  for (const swap of swaps) {
    const next: Swap[][] = []
    for (const combo of out) {
      next.push(combo)
      if (!combo.some((item) => item.removesPantry === swap.removesPantry)) {
        next.push([...combo, swap])
      }
    }
    out = next
  }
  return out
}

function applySwaps(base: RecipeLine[], swaps: Swap[], foods: Map<string, Food>): RecipeLine[] | null {
  let lines = base.filter((line) => !line.optional)
  for (const swap of swaps) {
    const removed = lines.filter((line) => line.pantryId === swap.removesPantry)
    if (removed.length === 0) return null
    const removedGrams = removed.reduce((sum, line) => sum + (line.grams ?? 0), 0)
    const removedCount = removed.reduce((sum, line) => sum + (line.count || 1), 0)
    lines = lines.filter((line) => line.pantryId !== swap.removesPantry)
    for (const add of swap.adds) {
      const food = foods.get(add.foodId)
      if (!food) return null
      const grams =
        add.grams ??
        (add.gramsEach != null ? add.gramsEach * removedCount : removedGrams)
      lines.push({
        foodId: add.foodId,
        pantryId: food.pantryId,
        amount: swap.label,
        grams: Math.round(grams * 100) / 100,
        count: 1,
        optional: false,
        gramNote: swap.source,
      })
    }
  }
  return lines
}

function isUnsafe(lines: RecipeLine[], foods: Map<string, Food>, allergies: AllergyId[]): boolean {
  const on = new Set(allergies)
  return lines.some((line) => {
    const food = foods.get(line.foodId)
    if (!food) return false
    if (food.allergens.some((item) => on.has(item as AllergyId))) return true
    return on.has("gluten") && food.glutenRisk
  })
}

export function planRecipe(
  recipe: Recipe,
  pantry: Set<string>,
  allergies: AllergyId[],
  foods: Map<string, Food>,
): Plan {
  // Hide the written recipe. A swap does not bring it back: kid mode still names the original food.
  if (isUnsafe(recipe.lines, foods, allergies)) {
    const lines = recipe.lines.filter((line) => !line.optional)
    const total = sumLines(lines, foods)
    return {
      fit: "hidden",
      missing: [],
      swaps: [],
      lines,
      math: lines.map((line) => lineMath(line, foods)),
      perServing: perServing(total, recipe.servings),
    }
  }

  let best: { missing: string[]; swaps: Swap[]; lines: RecipeLine[] } | null = null
  for (const combo of combos(recipe.swaps)) {
    const lines = combo.length === 0 ? recipe.lines.filter((line) => !line.optional) : applySwaps(recipe.lines, combo, foods)
    if (!lines) continue
    if (isUnsafe(lines, foods, allergies)) continue
    const missing = [...new Set(lines.map((line) => line.pantryId))].filter((id) => !pantry.has(id))
    const candidate = { missing, swaps: combo, lines }
    if (
      !best ||
      candidate.missing.length < best.missing.length ||
      (candidate.missing.length === best.missing.length && candidate.swaps.length < best.swaps.length)
    ) {
      best = candidate
    }
  }

  if (!best) {
    const lines = recipe.lines.filter((line) => !line.optional)
    const total = sumLines(lines, foods)
    return {
      fit: "hidden",
      missing: [],
      swaps: [],
      lines,
      math: lines.map((line) => lineMath(line, foods)),
      perServing: perServing(total, recipe.servings),
    }
  }

  const haveSome = best.lines.some((line) => pantry.has(line.pantryId))
  const fit: Fit = best.missing.length === 0 ? "now" : best.missing.length <= 2 && haveSome ? "almost" : "later"
  const total = sumLines(best.lines, foods)
  return {
    fit,
    missing: best.missing,
    swaps: best.swaps,
    lines: best.lines,
    math: best.lines.map((line) => lineMath(line, foods)),
    perServing: perServing(total, recipe.servings),
  }
}

export function bestUnlock(
  owned: Set<string>,
  allergies: AllergyId[],
  foods: Map<string, Food>,
  choices: { id: string; name: string }[],
  allRecipes: Recipe[],
): { id: string; name: string; count: number } | null {
  const visible = (pantry: Set<string>) =>
    allRecipes.reduce((count, recipe) => {
      const fit = planRecipe(recipe, pantry, allergies, foods).fit
      return fit === "now" || fit === "almost" ? count + 1 : count
    }, 0)
  const already = visible(owned)
  let best: { id: string; name: string; count: number } | null = null
  for (const choice of choices) {
    if (owned.has(choice.id)) continue
    const next = new Set(owned)
    next.add(choice.id)
    const count = visible(next) - already
    if (count > 0 && (!best || count > best.count)) best = { id: choice.id, name: choice.name, count }
  }
  return best
}
