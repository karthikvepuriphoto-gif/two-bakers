import { formatNutrient } from "../lib/nutrition.ts"
import type { Nutrients } from "../data/types.ts"

export function NutrientHero({ nutrients, servingLabel }: { nutrients: Nutrients; servingLabel: string }) {
  const proteinPct = Math.min(100, (nutrients.protein / 20) * 100)
  const fiberPct = Math.min(100, (nutrients.fiber / 8) * 100)
  return (
    <section className="grid gap-3" aria-label="Protein and fiber per serving">
      <p className="text-sm font-extrabold text-ink/70">Each {servingLabel}</p>
      <div className="grid grid-cols-2 gap-3">
        <Meter
          label="Protein"
          value={`${formatNutrient(nutrients.protein)} g`}
          hint="20 g fills the bar"
          percent={proteinPct}
          tone="coral"
        />
        <Meter
          label="Fiber"
          value={`${formatNutrient(nutrients.fiber)} g`}
          hint="8 g fills the bar"
          percent={fiberPct}
          tone="leaf"
        />
      </div>
      <div className="grid grid-cols-2 gap-3">
        <SmallStat label="Calories" value={formatNutrient(nutrients.kcal, 0)} />
        <SmallStat label="Sugar" value={`${formatNutrient(nutrients.sugar)} g`} />
      </div>
    </section>
  )
}

function Meter({
  label,
  value,
  hint,
  percent,
  tone,
}: {
  label: string
  value: string
  hint: string
  percent: number
  tone: "coral" | "leaf"
}) {
  const bar = tone === "coral" ? "bg-coral" : "bg-leaf"
  return (
    <div className="rounded-3xl bg-white p-3 shadow-sm">
      <p className="text-sm font-extrabold uppercase tracking-wide text-ink/60">{label}</p>
      <p className="font-display text-4xl leading-none text-ink">{value}</p>
      <div className="mt-3 h-4 overflow-hidden rounded-full bg-cream" role="img" aria-label={`${label} meter, ${hint}`}>
        <div className={`h-full rounded-full ${bar}`} style={{ width: `${percent}%` }} />
      </div>
      <p className="mt-1 text-xs font-bold text-ink/60">{hint}</p>
    </div>
  )
}

function SmallStat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl bg-white/80 px-3 py-2">
      <p className="text-xs font-extrabold uppercase tracking-wide text-ink/50">{label}</p>
      <p className="font-display text-2xl text-ink">{value}</p>
    </div>
  )
}

const GROWNUP: Record<string, string> = {
  oven: "Hot oven",
  stove: "Hot stove",
  knife: "Sharp knife",
  microwave: "Hot microwave",
}

export function GrownupBadges({ kinds }: { kinds: string[] }) {
  if (kinds.length === 0) return null
  return (
    <ul className="flex flex-wrap gap-2">
      {kinds.map((kind) => (
        <li key={kind} className="rounded-full bg-sun px-3 py-1 text-sm font-extrabold text-ink">
          Ask a grown-up · {GROWNUP[kind] ?? kind}
        </li>
      ))}
    </ul>
  )
}
