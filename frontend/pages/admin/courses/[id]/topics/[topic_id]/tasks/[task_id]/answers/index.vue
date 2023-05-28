<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
                <ControlButtonCreate />
            </template>
        </ControlPanel>
        <CommonContent>
            <CommonListViewTable :items="data!.items" link-param-name="answer_id" />
            <CommonLoadMore :response="data" @load-needed="loadMore" />
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const route = useRoute();

    const { data, loadMore } = await useListLoader({
        path: '/api/courses/{course_id}/topics/{topic_id}/tasks/{task_id}/answers/',
        method: 'get',
        params: {
            course_id: route.params.id as string,
            topic_id: route.params.topic_id as string,
            task_id: route.params.task_id as string,
        },
    });
</script>
