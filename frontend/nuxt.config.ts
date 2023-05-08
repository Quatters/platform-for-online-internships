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
    modules: ['@pinia/nuxt', '@pinia-plugin-persistedstate/nuxt', '@nuxtjs/i18n'],
    postcss: {
        plugins: {
            tailwindcss: {},
            autoprefixer: {},
        },
    },
    i18n: {
        vueI18n: './i18n.config.ts',
        locales: ['ru'],
        defaultLocale: 'ru',
        strategy: 'no_prefix',
    },
});
