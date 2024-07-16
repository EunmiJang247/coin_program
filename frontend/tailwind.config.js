/** @type {import('tailwindcss').Config} */
module.exports = {
  purge: ['./pages/**/*.{js,ts,jsx,tsx}', './components/**/*.{js,ts,jsx,tsx}'],
  content: [],
  theme: {
    extend: {},
    screens: {
      sm: '640px',
      md: '1024px',
      lg: '1280px',
    },
  },
  plugins: [],
};
