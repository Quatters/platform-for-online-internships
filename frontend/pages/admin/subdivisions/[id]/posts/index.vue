<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
                <ControlButtonCreate />
            </template>
            <template #inputs>
                <ControlSearchInput v-model="search" />
            </template>
        </ControlPanel>
        <CommonContent>
            <CommonListViewTable
                :items="data!.items"
                link-param-name="post_id"
                :additional-params="{ id: route.params.id as string }"
            />
            <CommonLoadMore :response="data" @load-needed="loadMore" />
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const route = useRoute();
    const { data, loadMore } = await useListLoader({
        path: '/api/subdivisions/{subdivision_id}/posts',
        method: 'get',
        params: { subdivision_id: route.params.id as string },
    });
    usePageStore().name = 'Должности';

    const search = ref<string | null | undefined>(getFirstQueryValue(route.query.search));
</script>
