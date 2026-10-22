import type { ReactNode } from "react"

interface Props {
  id: string
  className?: string
}

function Frame({ bg, children }: { bg: string; children: ReactNode }) {
  return (
    <svg viewBox="0 0 80 80" className="h-full w-full" aria-hidden="true">
      <rect width="80" height="80" rx="22" fill={bg} />
      {children}
    </svg>
  )
}

export function FoodArt({ id, className }: Props) {
  return (
    <div className={className}>
      <Picture id={id} />
    </div>
  )
}

function Picture({ id }: { id: string }) {
  switch (id) {
    case "banana":
      return (
        <Frame bg="#FFE08A">
          <path d="M22 24c10-12 32-10 38 8 4 14-6 30-22 32-8 1-16-6-16-14 0-8 6-12 8-18 2-6-2-8-8-8z" fill="#F5C400" />
          <path d="M24 28c8 2 14 10 16 20" stroke="#C48A00" strokeWidth="3" fill="none" strokeLinecap="round" />
          <circle cx="30" cy="34" r="2" fill="#5C3B00" />
        </Frame>
      )
    case "strawberries":
      return (
        <Frame bg="#FFD0DC">
          <path d="M40 22c8 8 16 18 14 32-1 8-8 12-14 12s-13-4-14-12C24 40 32 30 40 22z" fill="#E23B4A" />
          <path d="M28 30c6-8 10-10 12-12 2 2 6 4 12 12" fill="#2F9E44" />
          <circle cx="36" cy="46" r="1.6" fill="#fff" />
          <circle cx="44" cy="52" r="1.6" fill="#fff" />
          <circle cx="38" cy="58" r="1.6" fill="#fff" />
        </Frame>
      )
    case "blueberries":
      return (
        <Frame bg="#D9E8FF">
          <circle cx="32" cy="42" r="12" fill="#3D5AFE" />
          <circle cx="50" cy="38" r="11" fill="#304FFE" />
          <circle cx="44" cy="54" r="10" fill="#1A237E" />
          <path d="M28 34c4-6 10-6 14-2" stroke="#9FA8DA" strokeWidth="2" fill="none" />
        </Frame>
      )
    case "peanut-butter":
    case "almond-butter":
    case "sunflower-butter":
    case "powdered-peanut":
      return (
        <Frame bg={id === "sunflower-butter" ? "#FFF1C9" : id === "powdered-peanut" ? "#F3E6D4" : "#F6D7A8"}>
          <rect x="24" y="22" width="32" height="40" rx="8" fill="#C47B3A" />
          <rect x="28" y="16" width="24" height="12" rx="4" fill="#8D5524" />
          <ellipse cx="40" cy="46" rx="8" ry="10" fill="#E7B56A" />
        </Frame>
      )
    case "honey":
      return (
        <Frame bg="#FFE7A3">
          <path d="M30 24h20l4 10v24a8 8 0 0 1-8 8H34a8 8 0 0 1-8-8V34z" fill="#F0A202" />
          <rect x="32" y="18" width="16" height="8" rx="2" fill="#C47B00" />
          <path d="M34 40h12" stroke="#FFF3C4" strokeWidth="3" strokeLinecap="round" />
        </Frame>
      )
    case "maple":
      return (
        <Frame bg="#F8D7B0">
          <path d="M34 14c8 10 16 14 16 26a14 14 0 1 1-28 0c0-8 4-12 12-26z" fill="#C4622D" />
          <circle cx="36" cy="48" r="3" fill="#F6C9A0" />
        </Frame>
      )
    case "greek-yogurt":
    case "yogurt":
      return (
        <Frame bg="#E7F6FF">
          <path d="M26 28h28l-3 32a8 8 0 0 1-8 7H37a8 8 0 0 1-8-7z" fill="#F7FBFF" stroke="#7EC8E3" strokeWidth="3" />
          <path d="M30 28c2-8 18-8 20 0" fill="#fff" />
          <path d="M32 46h16" stroke="#9AD7EA" strokeWidth="3" strokeLinecap="round" />
        </Frame>
      )
    case "cottage-cheese":
      return (
        <Frame bg="#E8F8F2">
          <rect x="22" y="26" width="36" height="32" rx="10" fill="#FFF" stroke="#7DCEA0" strokeWidth="3" />
          <circle cx="34" cy="40" r="4" fill="#F4F7F2" stroke="#B7E4C7" />
          <circle cx="46" cy="44" r="5" fill="#F4F7F2" stroke="#B7E4C7" />
          <circle cx="38" cy="50" r="3" fill="#F4F7F2" stroke="#B7E4C7" />
        </Frame>
      )
    case "milk":
    case "almond-milk":
      return (
        <Frame bg={id === "milk" ? "#EAF4FF" : "#F4EFE4"}>
          <path d="M30 18h14l4 8v32a6 6 0 0 1-6 6H32a6 6 0 0 1-6-6V26z" fill={id === "milk" ? "#D6ECFF" : "#E7D3B0"} />
          <rect x="34" y="34" width="12" height="16" rx="2" fill="#fff" />
        </Frame>
      )
    case "egg":
      return (
        <Frame bg="#FFF4D8">
          <ellipse cx="40" cy="44" rx="16" ry="20" fill="#FFFDF8" stroke="#E6C98A" strokeWidth="3" />
          <ellipse cx="40" cy="46" rx="7" ry="8" fill="#F5C451" />
        </Frame>
      )
    case "mozzarella":
      return (
        <Frame bg="#FFF3C4">
          <path d="M22 36c6-12 30-12 36 0v16c-6 10-30 10-36 0z" fill="#FFE08A" />
          <circle cx="34" cy="42" r="4" fill="#FFF6D0" />
          <circle cx="48" cy="46" r="3" fill="#FFF6D0" />
        </Frame>
      )
    case "butter":
      return (
        <Frame bg="#FFF1B8">
          <rect x="20" y="32" width="40" height="22" rx="4" fill="#FFE56A" stroke="#E2B93B" strokeWidth="3" />
          <path d="M20 40h40" stroke="#F6D34D" strokeWidth="3" />
        </Frame>
      )
    case "oats":
      return (
        <Frame bg="#F3E2C4">
          <ellipse cx="28" cy="44" rx="10" ry="6" fill="#E0B15A" transform="rotate(-20 28 44)" />
          <ellipse cx="44" cy="36" rx="10" ry="6" fill="#C9842A" transform="rotate(15 44 36)" />
          <ellipse cx="50" cy="50" rx="10" ry="6" fill="#A86B2A" transform="rotate(-10 50 50)" />
          <ellipse cx="34" cy="54" rx="9" ry="5" fill="#D9A441" transform="rotate(20 34 54)" />
        </Frame>
      )
    case "flour":
    case "whole-wheat":
    case "almond-flour":
      return (
        <Frame bg={id === "whole-wheat" ? "#EAD7C1" : id === "almond-flour" ? "#F6E3C4" : "#F7F1E6"}>
          <path d="M24 30h32v8c0 16-6 26-16 26S24 54 24 38z" fill={id === "whole-wheat" ? "#C4A484" : "#FBF7F1"} stroke="#C8B59A" strokeWidth="3" />
          <path d="M30 30c2-8 18-8 20 0" fill="#EFE6D6" />
        </Frame>
      )
    case "baking-powder":
    case "baking-soda":
      return (
        <Frame bg={id === "baking-soda" ? "#FFE0CC" : "#E4F7EA"}>
          <rect x="28" y="18" width="24" height="46" rx="6" fill={id === "baking-soda" ? "#F4A261" : "#74C69D"} />
          <rect x="32" y="28" width="16" height="18" rx="2" fill="#fff" />
        </Frame>
      )
    case "vanilla":
      return (
        <Frame bg="#F8E7C9">
          <rect x="34" y="16" width="12" height="48" rx="6" fill="#6B3F1D" />
          <rect x="36" y="28" width="8" height="16" fill="#E7C59A" />
          <circle cx="40" cy="18" r="4" fill="#3E2412" />
        </Frame>
      )
    case "cinnamon":
    case "oregano":
    case "onion-powder":
    case "garlic-powder":
      return (
        <Frame bg={id === "cinnamon" ? "#F6D3B0" : id === "oregano" ? "#D8F3DC" : "#F1E4D4"}>
          <rect x="30" y="20" width="20" height="42" rx="8" fill={id === "oregano" ? "#40916C" : "#A47148"} />
          <circle cx="40" cy="30" r="6" fill="#F8EDE3" />
        </Frame>
      )
    case "salt":
      return (
        <Frame bg="#F4F7FB">
          <path d="M32 22h16l4 12v22a8 8 0 0 1-8 8H36a8 8 0 0 1-8-8V34z" fill="#D7DEE8" />
          <circle cx="36" cy="48" r="2" fill="#fff" />
          <circle cx="44" cy="44" r="2" fill="#fff" />
          <circle cx="42" cy="54" r="2" fill="#fff" />
        </Frame>
      )
    case "cocoa":
      return (
        <Frame bg="#E7D3C5">
          <rect x="26" y="24" width="28" height="36" rx="6" fill="#5C3317" />
          <rect x="30" y="18" width="20" height="10" rx="3" fill="#7A4A28" />
          <circle cx="40" cy="44" r="6" fill="#3B1F0E" />
        </Frame>
      )
    case "brown-sugar":
      return (
        <Frame bg="#F6E0C8">
          <path d="M24 36c4-14 28-14 32 0v18c-4 10-28 10-32 0z" fill="#C68642" />
          <ellipse cx="40" cy="36" rx="16" ry="6" fill="#E0A15A" />
        </Frame>
      )
    case "protein-powder":
      return (
        <Frame bg="#E4F0FF">
          <rect x="26" y="20" width="28" height="42" rx="8" fill="#4C6EF5" />
          <path d="M32 36h16l-2 16H34z" fill="#EDF2FF" />
          <path d="M34 46h10" stroke="#4C6EF5" strokeWidth="3" strokeLinecap="round" />
        </Frame>
      )
    case "chocolate":
      return (
        <Frame bg="#EBD3C4">
          <rect x="22" y="28" width="36" height="28" rx="4" fill="#5C3317" />
          <path d="M22 38h36M34 28v28M46 28v28" stroke="#8A5A34" strokeWidth="2" />
        </Frame>
      )
    case "raisins":
      return (
        <Frame bg="#F0D8C8">
          <ellipse cx="32" cy="40" rx="8" ry="10" fill="#6B3A2A" transform="rotate(-15 32 40)" />
          <ellipse cx="46" cy="36" rx="7" ry="9" fill="#4A2418" transform="rotate(10 46 36)" />
          <ellipse cx="44" cy="52" rx="8" ry="9" fill="#7A4633" />
        </Frame>
      )
    case "coconut":
      return (
        <Frame bg="#E7F6F2">
          <circle cx="40" cy="42" r="18" fill="#F7F3EA" stroke="#C4B7A6" strokeWidth="3" />
          <circle cx="34" cy="40" r="2" fill="#6B5344" />
          <circle cx="46" cy="40" r="2" fill="#6B5344" />
          <path d="M34 48c4 4 8 4 12 0" stroke="#6B5344" strokeWidth="2" fill="none" />
        </Frame>
      )
    case "granola":
      return (
        <Frame bg="#F8E3C4">
          <path d="M24 48 34 28l8 16 6-10 10 18z" fill="#E09F3E" />
          <circle cx="30" cy="52" r="4" fill="#BB6B2D" />
          <circle cx="48" cy="54" r="5" fill="#A15C2A" />
        </Frame>
      )
    case "walnuts":
      return (
        <Frame bg="#F3E0C8">
          <path d="M28 28c8 4 8 12 0 16 10 2 16 10 8 18 8-2 18-8 16-18-6-2-6-10 0-16-8 2-16 0-24 0z" fill="#8C5A34" />
        </Frame>
      )
    case "coconut-oil":
    case "olive-oil":
      return (
        <Frame bg={id === "olive-oil" ? "#E5F4D8" : "#FFF6D8"}>
          <path d="M34 16h12v8l6 8v28a8 8 0 0 1-8 8H36a8 8 0 0 1-8-8V32l6-8z" fill={id === "olive-oil" ? "#7CB342" : "#F2E28A"} />
          <rect x="36" y="12" width="8" height="6" fill="#8D6E63" />
        </Frame>
      )
    case "bacon":
      return (
        <Frame bg="#FFD8CC">
          <path d="M18 34c10-6 14 6 24 0s14 6 22 0v8c-8 6-12-6-22 0s-14-6-24 0z" fill="#E76F51" />
          <path d="M18 46c10-6 14 6 24 0s14 6 22 0v6c-8 6-12-6-22 0s-14-6-24 0z" fill="#F4A261" />
        </Frame>
      )
    case "rice-paper":
      return (
        <Frame bg="#E8F7FF">
          <circle cx="40" cy="42" r="18" fill="none" stroke="#7FDBDA" strokeWidth="6" />
          <circle cx="40" cy="42" r="8" fill="none" stroke="#B2F0EA" strokeWidth="4" />
        </Frame>
      )
    default:
      return (
        <Frame bg="#FFE8D6">
          <circle cx="40" cy="40" r="14" fill="#E25B3A" />
        </Frame>
      )
  }
}
