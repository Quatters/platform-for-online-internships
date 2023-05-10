import { APIPath, APIMethod, LoaderArgs } from '~/types';

export default async function <P extends APIPath, M extends APIMethod<P>>({ path, method }: { path: P; method: M }) {
    const { $api } = useNuxtApp();
    const config = useRuntimeConfig();

    const loader = ({ limit, offset }: LoaderArgs = {}) =>
        $api({
            path,
            method,
            query: {
                limit,
                offset,
            },
        });

    const { data } = await useAsyncData(() => loader({ limit: config.public.pageSize }));

    async function loadMore(params: LoaderArgs) {
        const newData = await loader(params);
        // @ts-expect-error expecting list path
        data.value = {
            ...newData,
            // @ts-expect-error expecting list path
            items: [...data.value!.items, ...newData.items],
        };
    }

    return {
        data,
        loadMore,
        loader,
    };
}
