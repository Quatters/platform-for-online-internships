<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonCreate />
            </template>
        </ControlPanel>
        <CommonContent>
            <CommonListViewTable :items="data!.items" />
            <CommonLoadMore :response="data" @load-needed="loadMore" />
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const { data, loadMore } = await useListLoader({ path: '/api/courses/', method: 'get' });
    usePageStore().name = 'Курсы';
</script>
