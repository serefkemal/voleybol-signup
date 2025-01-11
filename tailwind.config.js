/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./app/static/js/**/*.{js,jsx}"],
    theme: {
      extend: {
        fontFamily: {
          'filsonsoft': ['FilsonSoft', 'sans-serif'],
        },
      },
    },
    plugins: [require("tailwindcss-animate")],
  }