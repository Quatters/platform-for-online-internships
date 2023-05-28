import type { RouteLocationNamedRaw } from 'vue-router';
import { defineStore } from 'pinia';
import { Breadcrumb } from '~/types';

interface ExtendedRouteLocationNamedRaw extends RouteLocationNamedRaw {
    response?: any;
    viewFieldName?: string;
    routerToResponseParamsMap?: Record<string, string>;
}

type FkInstancePathMap = Record<string, ExtendedRouteLocationNamedRaw>;

export default defineStore('page', () => {
    const fkInstancePathMap = ref<FkInstancePathMap>({});
    const breadcrumbs = ref<Breadcrumb[]>([]);

    return {
        fkInstancePathMap,
        breadcrumbs,
    };
});
