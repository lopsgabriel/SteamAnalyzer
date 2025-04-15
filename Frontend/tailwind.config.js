/** @type {import('tailwindcss').Config} */

const daisyui = require("daisyui");
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    "./app/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        josefin: ['JosefinSans', 'sans-serif'],
        bebastech: ['Bebas Neue', 'sans-serif'],
        onest: ['Onest', 'sans-serif'],
        orbitron: ['Orbitron', 'sans-serif'],
        sharetech: ['Share Tech Mono', 'monospace'],
        sora: ['Sora', 'sans-serif'],
      }
    },
  },
  plugins: [daisyui, require("tailwindcss-animate")],
};
