import type { LocationQuery } from 'vue-router';
import { APIPath, APIMethod, LoaderArgs } from '~/types';

export default async function <P extends APIPath, M extends APIMethod<P>>({
    path,
    method,
    params,
}: {
    path: P;
    method: M;
    params?: Record<string, string | number>;
    watchQuery?: Record<string, Ref<string | undefined>>;
}) {
    const { $api } = useNuxtApp();
    const config = useRuntimeConfig();
    const route = useRoute();

    function filterRouteQuery(newQuery: LocationQuery) {
        return Object.fromEntries(Object.entries(newQuery).filter(([key]) => !['limit', 'offset'].includes(key)));
    }

    const loader = ({ limit, offset }: LoaderArgs = {}) => {
        return $api({
            path,
            method,
            query: {
                ...filterRouteQuery(route.query),
                limit,
                offset,
            },
            params,
        });
    };

    const data = ref(await loader({ limit: config.public.pageSize }));

    async function loadMore({ limit, offset }: LoaderArgs) {
        const newData = await loader({ limit, offset });
        // @ts-expect-error expecting list path
        data.value = {
            ...newData,
            // @ts-expect-error expecting list path
            items: [...data.value!.items, ...newData.items],
        };
    }

    watch(toRef(route, 'query'), async newQuery => {
        const filtered = filterRouteQuery(newQuery);
        // @ts-expect-error expecting list path
        data.value = await $api({
            path,
            method,
            query: {
                ...filtered,
                limit: config.public.pageSize,
            },
        });
    });

    return {
        data,
        loadMore,
        loader,
    };
}
