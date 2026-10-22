import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"
import tailwindcss from "@tailwindcss/vite"
import { VitePWA } from "vite-plugin-pwa"

export default defineConfig({
  base: "/two-bakers/",
  plugins: [
    react(),
    tailwindcss(),
    VitePWA({
      registerType: "autoUpdate",
      includeAssets: ["favicon.svg", "icon-192.png", "icon-512.png"],
      scope: "/two-bakers/",
      manifest: {
        name: "Two Bakers",
        short_name: "Two Bakers",
        description: "Kid snack recipes for Karthik's daughter and son, counted from USDA FoodData Central.",
        theme_color: "#c13a22",
        background_color: "#fff6ea",
        display: "standalone",
        lang: "en",
        id: "/two-bakers/",
        start_url: "/two-bakers/",
        scope: "/two-bakers/",
        icons: [
          { src: "icon-192.png", sizes: "192x192", type: "image/png" },
          { src: "icon-512.png", sizes: "512x512", type: "image/png", purpose: "any maskable" },
        ],
      },
      workbox: {
        globPatterns: ["**/*.{js,css,html,svg,png,woff,woff2}"],
        navigateFallback: "/two-bakers/index.html",
      },
    }),
  ],
})
