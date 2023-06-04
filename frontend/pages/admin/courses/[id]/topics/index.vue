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
            <CommonListViewTable :items="data!.items" link-param-name="topic_id" />
            <CommonLoadMore :response="data" @load-needed="loadMore" />
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const route = useRoute();

    const { data, loadMore } = await useListLoader({
        path: '/api/courses/{course_id}/topics/',
        method: 'get',
        params: {
            course_id: route.params.id as string,
        },
    });

    const search = ref<string | null | undefined>(getFirstQueryValue(route.query.search));
</script>
