/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./templates/**/*.html",  // Path ke file template Django
        "./**/*.py",              // Jika Anda menyisipkan CSS di file Python
        "./static/javascript/**/*.js",    // Path ke file JS (jika ada)
    ],

    theme: {
        extend: {},
    },
    plugins: [],
}

