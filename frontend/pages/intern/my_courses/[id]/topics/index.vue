<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
            </template>
        </ControlPanel>
        <CommonContent>
            <CommonListViewTable :items="data!.items" link-param-name="topic_id" hide-head />
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
</script>
