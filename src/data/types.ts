export interface Nutrients {
  kcal: number
  protein: number
  fiber: number
  sugar: number
}

export interface Food {
  id: string
  pantryId: string
  name: string
  fdcId: number | null
  fdcName: string | null
  dataset: string | null
  fdcUrl: string | null
  per100g: Nutrients | null
  allergens: string[]
  glutenRisk: boolean
  note: string
}

export interface PantryItem {
  id: string
  name: string
  group: string
  hint: string
}

export interface RecipeLine {
  foodId: string
  pantryId: string
  amount: string
  grams: number | null
  count: number
  optional: boolean
  gramNote: string
}

export interface SwapAdd {
  foodId: string
  grams?: number
  gramsEach?: number | null
}

export interface Swap {
  id: string
  removesPantry: string
  label: string
  source: string
  author: boolean
  sameGrams: boolean
  adds: SwapAdd[]
}

export interface Step {
  text: string
  timerSec?: number
  timerLabel?: string
  grownup: string[]
}

export interface Recipe {
  id: string
  title: string
  category: string
  blurb: string
  servings: number
  servingLabel: string
  minutes: number
  heat: string
  sourceName: string
  sourceUrl: string
  author: string
  lines: RecipeLine[]
  swaps: Swap[]
  unquantified: string[]
  steps: Step[]
}

export type AllergyId = "peanut" | "dairy" | "egg" | "gluten"

export interface MadeStamp {
  id: string
  recipeId: string
  sticker: string
  at: number
}

export interface Saved {
  pantry: string[]
  allergies: AllergyId[]
  favorites: string[]
  made: MadeStamp[]
  quiet: boolean
}
