<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonCreate />
            </template>
            <template #inputs>
                <ControlSearchInput v-model="search" />
            </template>
        </ControlPanel>
        <CommonContent>
            <CommonListViewTable :items="data!.items" />
            <CommonLoadMore :response="data" @load-needed="loadMore" />
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const { data, loadMore } = await useListLoader({ path: '/api/subdivisions/', method: 'get' });
    usePageStore().name = 'Подразделения';

    const route = useRoute();

    const search = ref<string | null | undefined>(getFirstQueryValue(route.query.search));
</script>
