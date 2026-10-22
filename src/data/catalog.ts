import foodsJson from "./foods.json" with { type: "json" }
import pantryJson from "./pantry.json" with { type: "json" }
import recipesJson from "./recipes.json" with { type: "json" }
import type { Food, PantryItem, Recipe } from "./types.ts"

export const foods = foodsJson as Food[]
export const pantry = pantryJson as PantryItem[]
export const recipes = recipesJson as Recipe[]

export const foodMap = new Map(foods.map((food) => [food.id, food]))
export const pantryMap = new Map(pantry.map((item) => [item.id, item]))

export const GROUPS = [...new Set(pantry.map((item) => item.group))]

export const STARTER = [
  "banana",
  "oats",
  "peanut-butter",
  "egg",
  "greek-yogurt",
  "cottage-cheese",
  "chocolate",
  "baking-powder",
  "vanilla",
  "cinnamon",
  "honey",
  "salt",
]

export const STICKERS = [
  { id: "star", label: "Gold star", glyph: "★" },
  { id: "cupcake", label: "Cupcake", glyph: "🧁" },
  { id: "rainbow", label: "Rainbow", glyph: "🌈" },
  { id: "trophy", label: "Trophy", glyph: "🏆" },
  { id: "heart", label: "Heart", glyph: "♥" },
  { id: "banana", label: "Banana", glyph: "🍌" },
]

export const ALLERGIES = [
  { id: "peanut" as const, label: "Peanut", detail: "Hides peanut butter and peanut flour." },
  { id: "dairy" as const, label: "Dairy", detail: "Hides milk, yogurt, cheese, butter, whey, and most chocolate chips." },
  { id: "egg" as const, label: "Egg", detail: "Hides recipes that still use eggs after a safe swap." },
  { id: "gluten" as const, label: "Gluten", detail: "Hides wheat flour and oats. Oats are often packed near wheat." },
]
