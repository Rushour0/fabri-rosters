import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// base: served from https://rushour0.github.io/fabri-rosters/ (project pages),
// so asset URLs and import.meta.env.BASE_URL resolve under /fabri-rosters/.
export default defineConfig({
  base: "/fabri-rosters/",
  plugins: [react()],
});
