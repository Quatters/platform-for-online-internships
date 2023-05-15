/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './components/**/*.{js,vue,ts}',
        './layouts/**/*.vue',
        './pages/**/*.vue',
        './plugins/**/*.{js,ts}',
        './nuxt.config.{js,ts}',
        './app.vue',
        'node_modules/tailvue/dist/tailvue.es.js',
    ],
    theme: {
        extend: {},
    },
    plugins: [],
    darkMode: 'class',
};
