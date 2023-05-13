import { APIPath, APIMethod, LoaderArgs } from '~/types';

export default async function <P extends APIPath, M extends APIMethod<P>>({
    path,
    method,
    params,
    watchQuery,
}: {
    path: P;
    method: M;
    params?: Record<string, string | number>;
    watchQuery?: Record<string, Ref<string | undefined>>;
}) {
    const { $api } = useNuxtApp();
    const config = useRuntimeConfig();

    function unpackWatchQuery() {
        return Object.fromEntries(
            Object.entries(watchQuery ?? ({} as Record<string, Ref<string | undefined>>)).map(([key, value]) => [
                key,
                value.value,
            ]),
        );
    }

    const loader = ({ limit, offset }: LoaderArgs = {}) => {
        const queries = unpackWatchQuery();

        return $api({
            path,
            method,
            query: {
                ...queries,
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

    if (watchQuery) {
        for (const [key, refValue] of Object.entries(watchQuery)) {
            watch(refValue, async newValue => {
                const queries = unpackWatchQuery();

                // @ts-expect-error expecting list path
                data.value = await $api({
                    path,
                    method,
                    query: {
                        ...queries,
                        [key]: newValue,
                        limit: config.public.pageSize,
                    },
                });
            });
        }
    }

    return {
        data,
        loadMore,
        loader,
    };
}
