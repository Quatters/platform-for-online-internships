import type { RouteLocationNamedRaw } from 'vue-router';
import { defineStore } from 'pinia';
import { Breadcrumb } from '~/types';

type FkInstancePathMap = Record<string, RouteLocationNamedRaw>;

export default defineStore('page', () => {
    const fkInstancePathMap = ref<FkInstancePathMap>({});
    const breadcrumbs = ref<Breadcrumb[]>([]);

    return {
        fkInstancePathMap,
        breadcrumbs,
    };
});
