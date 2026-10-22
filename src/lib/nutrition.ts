import type { Food, Nutrients, RecipeLine } from "../data/types.ts"

export const ZERO: Nutrients = { kcal: 0, protein: 0, fiber: 0, sugar: 0 }

export function addNutrients(a: Nutrients, b: Nutrients): Nutrients {
  return {
    kcal: a.kcal + b.kcal,
    protein: a.protein + b.protein,
    fiber: a.fiber + b.fiber,
    sugar: a.sugar + b.sugar,
  }
}

export function scaleNutrients(per100: Nutrients, grams: number): Nutrients {
  const factor = grams / 100
  return {
    kcal: per100.kcal * factor,
    protein: per100.protein * factor,
    fiber: per100.fiber * factor,
    sugar: per100.sugar * factor,
  }
}

export interface LineMath {
  line: RecipeLine
  food: Food
  amount: Nutrients | null
}

export function lineMath(line: RecipeLine, foods: Map<string, Food>): LineMath {
  const food = foods.get(line.foodId)
  if (!food) throw new Error(`Missing food ${line.foodId}`)
  if (line.grams == null || !food.per100g) return { line, food, amount: null }
  return { line, food, amount: scaleNutrients(food.per100g, line.grams) }
}

export function sumLines(lines: RecipeLine[], foods: Map<string, Food>): Nutrients {
  return lines.reduce((total, line) => {
    const row = lineMath(line, foods)
    return row.amount ? addNutrients(total, row.amount) : total
  }, ZERO)
}

export function perServing(total: Nutrients, servings: number): Nutrients {
  return {
    kcal: total.kcal / servings,
    protein: total.protein / servings,
    fiber: total.fiber / servings,
    sugar: total.sugar / servings,
  }
}

export function formatGrams(value: number): string {
  const rounded = Math.round(value * 100) / 100
  return Number.isInteger(rounded) ? String(rounded) : rounded.toFixed(2).replace(/0+$/, "").replace(/\.$/, "")
}

export function formatNutrient(value: number, digits = 1): string {
  return (Math.round(value * 10 ** digits) / 10 ** digits).toFixed(digits)
}
