/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#080c10',
        panel: '#0d1117',
        border: '#1e2d3d',
        bull: '#00ff88',
        bear: '#ff3d5a',
        neutral: '#f5a623',
        info: '#00cfff',
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'IBM Plex Mono', 'monospace'],
        display: ['Syne', 'Chakra Petch', 'sans-serif'],
      },
    },
  },
  plugins: [
    require("tailwindcss-animate"),
  ],
}
