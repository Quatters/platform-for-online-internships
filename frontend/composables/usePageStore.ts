import type { RouteLocationNamedRaw } from 'vue-router';
import { defineStore } from 'pinia';

type FkInstancePathMap = Record<string, RouteLocationNamedRaw>;

export default defineStore('page', () => {
    const name = ref('');
    const fkInstancePathMap = ref<FkInstancePathMap>({});

    return {
        name,
        fkInstancePathMap,
    };
});
