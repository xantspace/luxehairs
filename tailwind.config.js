/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './shop/templates/**/*.html',
    './*/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        'luxe-purple': '#4A1C6C',
        'luxe-purple-light': '#5B2C83',
        'luxe-gold': '#D4AF37',
        'luxe-gold-light': '#C9A961',
        'luxe-cream': '#D4B896',
        'luxe-tan': '#C9A589',
        'luxe-silver': '#A8B0BC',
        'luxe-navy': '#1C1A3A',
      },
      fontFamily: {
        playfair: ['"Playfair Display"', 'serif'],
        script: ['"Playfair Script"', 'cursive'],
        inter: ['"Inter"', 'sans-serif'],
      },
    },
  },
  plugins: [],
}