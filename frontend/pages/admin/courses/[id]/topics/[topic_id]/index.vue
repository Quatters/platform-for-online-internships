<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
                <ControlButtonEdit />
                <ControlButtonDelete
                    path="/api/courses/{course_id}/topics/{topic_id}"
                    :params="{ course_id: route.params.id as string, topic_id: route.params.topic_id as string}"
                />
            </template>
            <template #links>
                <NuxtLink
                    :to="{ name: 'admin-courses-id-topics-topic_id-tasks', params: { id: route.params.id, topic_id: route.params.topic_id as string} }"
                    class="btn-link"
                >
                    Задания
                </NuxtLink>
                <NuxtLink
                    :to="{ name: 'admin-courses-id-topics-topic_id-resources', params: { id: route.params.id, topic_id: route.params.topic_id as string} }"
                    class="btn-link"
                >
                    Ресурсы
                </NuxtLink>
            </template>
        </ControlPanel>
        <CommonContent>
            <CommonDetailViewCard :item="data!" :hide-fields="['course_id']" />
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const route = useRoute();

    const pageStore = usePageStore();
    pageStore.fkInstancePathMap = {
        prev_topic: { name: 'admin-courses-id-topics-topic_id', params: { id: route.params.id as string } },
        next_topic: { name: 'admin-courses-id-topics-topic_id', params: { id: route.params.id as string } },
    };

    const { $api } = useNuxtApp();

    const { data } = await useAsyncData(() => {
        return $api({
            path: '/api/courses/{course_id}/topics/{topic_id}',
            method: 'get',
            params: { course_id: route.params.id as string, topic_id: route.params.topic_id as string },
        });
    });
</script>
