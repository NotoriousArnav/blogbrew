/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/*.html',
    './templates/**/*.html',
    './static/**/*.{css,js}',
    './static/*.{css,js}'
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

