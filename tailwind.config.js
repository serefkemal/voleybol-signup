/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./app/static/js/**/*.{js,jsx}"],
    theme: {
      extend: {},
    },
    plugins: [require("tailwindcss-animate")],
  }