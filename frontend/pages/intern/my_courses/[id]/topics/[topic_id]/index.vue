<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
            </template>
        </ControlPanel>
        <CommonContent>
            <InternNameDescriptionCard :name="data!.name" :description="data!.description">
                <template #additional-content>
                    <div class="flex justify-between">
                        <div>
                            <NuxtLink
                                v-if="data?.prev_topic"
                                :to="{
                                    name: 'intern-my_courses-id-topics-topic_id',
                                    params: { id: route.params.id, topic_id: data.prev_topic?.id },
                                }"
                                class="link"
                            >
                                Предыдущая тема
                            </NuxtLink>
                        </div>
                        <div>
                            <NuxtLink
                                v-if="data?.next_topic"
                                :to="{
                                    name: 'intern-my_courses-id-topics-topic_id',
                                    params: { id: route.params.id, topic_id: data.next_topic.id },
                                }"
                                class="link"
                            >
                                Следующая тема
                            </NuxtLink>
                        </div>
                    </div>
                </template>
            </InternNameDescriptionCard>
            <div class="mt-4">
                <TopicResourcesList :items="resources.items" />
                <CommonLoadMore :response="resources" @load-needed="loadMore" />
            </div>
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const route = useRoute();

    const pageStore = usePageStore();
    pageStore.fkInstancePathMap = {
        prev_topic: { name: 'intern-my_courses-id-topics-topic_id', params: { id: route.params.id as string } },
        next_topic: { name: 'intern-my_courses-id-topics-topic_id', params: { id: route.params.id as string } },
    };

    const { $api } = useNuxtApp();

    const { data } = await useAsyncData(() => {
        return $api({
            path: '/api/courses/{course_id}/topics/{topic_id}',
            method: 'get',
            params: { course_id: route.params.id as string, topic_id: route.params.topic_id as string },
        });
    });

    const { data: resources, loadMore } = await useListLoader({
        path: '/api/courses/{course_id}/topics/{topic_id}/resources/',
        method: 'get',
        params: {
            course_id: route.params.id as string,
            topic_id: route.params.topic_id as string,
        },
    });
</script>
