<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
                <ControlButtonEdit />
                <ControlButtonDelete
                    path="/api/courses/{course_id}/topics/{topic_id}/resources/{resource_id}"
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
        resource_id: route.params.resource_id as string,
    };

    const pageStore = usePageStore();

    pageStore.fkInstancePathMap = {
        next_resource: {
            name: 'admin-courses-id-topics-topic_id-resources-resource_id',
            params: {
                id: route.params.id as string,
                topic_id: route.params.topic_id as string,
            },
        },
        prev_resource: {
            name: 'admin-courses-id-topics-topic_id-resources-resource_id',
            params: {
                id: route.params.id as string,
                topic_id: route.params.topic_id as string,
            },
        },
    };

    const { $api } = useNuxtApp();

    const { data } = await useAsyncData(() => {
        return $api({
            path: '/api/courses/{course_id}/topics/{topic_id}/resources/{resource_id}',
            method: 'get',
            params: apiParams,
        });
    });
</script>
