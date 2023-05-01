// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    typescript: {
        strict: true,
        typeCheck: true,
    },
    runtimeConfig: {
        public: {
            apiUrl: 'http://localhost:8000',
        },
    },
    app: {
        pageTransition: {
            name: 'page',
            mode: 'out-in',
        },
        layoutTransition: {
            name: 'page',
            mode: 'out-in',
        },
    },
    ssr: false,
    css: ['~/assets/css/main.css'],
    modules: ['@pinia/nuxt', '@pinia-plugin-persistedstate/nuxt'],
    postcss: {
        plugins: {
            tailwindcss: {},
            autoprefixer: {},
        },
    },
});
