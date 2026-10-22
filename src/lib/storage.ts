import { useEffect, useState } from "react"
import type { AllergyId, MadeStamp, Saved } from "../data/types.ts"

const KEY = "twobakers-v1"

const EMPTY: Saved = {
  pantry: [],
  allergies: [],
  favorites: [],
  made: [],
  quiet: false,
}

function load(): Saved {
  try {
    const raw = localStorage.getItem(KEY)
    if (!raw) return EMPTY
    const parsed = JSON.parse(raw) as Partial<Saved>
    return {
      pantry: parsed.pantry ?? [],
      allergies: parsed.allergies ?? [],
      favorites: parsed.favorites ?? [],
      made: parsed.made ?? [],
      quiet: parsed.quiet ?? false,
    }
  } catch {
    return EMPTY
  }
}

export function useSaved() {
  const [saved, setSaved] = useState<Saved>(() => load())

  useEffect(() => {
    localStorage.setItem(KEY, JSON.stringify(saved))
  }, [saved])

  function togglePantry(id: string) {
    setSaved((current) => ({
      ...current,
      pantry: current.pantry.includes(id)
        ? current.pantry.filter((item) => item !== id)
        : [...current.pantry, id],
    }))
  }

  function toggleAllergy(id: AllergyId) {
    setSaved((current) => ({
      ...current,
      allergies: current.allergies.includes(id)
        ? current.allergies.filter((item) => item !== id)
        : [...current.allergies, id],
    }))
  }

  function toggleFavorite(id: string) {
    setSaved((current) => ({
      ...current,
      favorites: current.favorites.includes(id)
        ? current.favorites.filter((item) => item !== id)
        : [...current.favorites, id],
    }))
  }

  function addMade(stamp: MadeStamp) {
    setSaved((current) => ({
      ...current,
      made: [stamp, ...current.made].slice(0, 200),
    }))
  }

  function setQuiet(quiet: boolean) {
    setSaved((current) => ({ ...current, quiet }))
  }

  function setPantry(pantry: string[]) {
    setSaved((current) => ({ ...current, pantry }))
  }

  function clearMade() {
    setSaved((current) => ({ ...current, made: [] }))
  }

  return { saved, togglePantry, toggleAllergy, toggleFavorite, addMade, setQuiet, setPantry, clearMade }
}
