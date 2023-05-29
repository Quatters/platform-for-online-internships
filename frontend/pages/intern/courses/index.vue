<template>
    <div>
        <ControlPanel>
            <template #inputs>
                <ControlSearchInput v-model="search" />
            </template>
        </ControlPanel>
        <CommonContent>
            <CommonListViewTable :items="data!.items" hide-head />
            <CommonLoadMore :response="data" @load-needed="loadMore" />
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const route = useRoute();

    const search = ref<string | null | undefined>(getFirstQueryValue(route.query.search));

    const { data, loadMore } = await useListLoader({
        path: '/api/courses/',
        method: 'get',
    });
</script>
