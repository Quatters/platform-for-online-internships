<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
                <ControlButtonEdit />
                <ControlButtonDelete
                    path="/api/courses/{course_id}/topics/{topic_id}/tasks/{task_id}/answers/{answer_id}"
                    :params="apiParams"
                />
            </template>
        </ControlPanel>
        <CommonContent>
            <CommonDetailViewCard :item="data!" />
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const route = useRoute();

    const apiParams = {
        course_id: route.params.id as string,
        topic_id: route.params.topic_id as string,
        task_id: route.params.task_id as string,
        answer_id: route.params.answer_id as string,
    };

    const { $api } = useNuxtApp();

    const { data } = await useAsyncData(() => {
        return $api({
            path: '/api/courses/{course_id}/topics/{topic_id}/tasks/{task_id}/answers/{answer_id}',
            method: 'get',
            params: apiParams,
        });
    });
</script>
