<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
                <ControlButtonEdit />
                <ControlButtonDelete
                    path="/api/courses/{course_id}/topics/{topic_id}/tasks/{task_id}"
                    :params="apiParams"
                />
            </template>
            <template #links>
                <NuxtLink
                    v-if="data?.task_type && ['single', 'multiple'].includes(data.task_type)"
                    :to="{
                        name: 'admin-courses-id-topics-topic_id-tasks-task_id-answers',
                        params: pageParams,
                    }"
                    class="link"
                >
                    Ответы
                </NuxtLink>
            </template>
        </ControlPanel>
        <CommonContent>
            <CommonDetailViewCard :item="data!" />
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const route = useRoute();

    const pageParams = {
        id: route.params.id as string,
        topic_id: route.params.topic_id as string,
        task_id: route.params.task_id as string,
    };

    const apiParams = {
        course_id: route.params.id as string,
        topic_id: route.params.topic_id as string,
        task_id: route.params.task_id as string,
    };

    const pageStore = usePageStore();
    pageStore.fkInstancePathMap = {
        prev_task: {
            name: 'admin-courses-id-topics-topic_id-tasks-task_id',
            params: pageParams,
        },
        next_task: {
            name: 'admin-courses-id-topics-topic_id-tasks-task_id',
            params: pageParams,
        },
    };

    const { $api } = useNuxtApp();

    const { data } = await useAsyncData(() => {
        return $api({
            path: '/api/courses/{course_id}/topics/{topic_id}/tasks/{task_id}',
            method: 'get',
            params: apiParams,
        });
    });
</script>
