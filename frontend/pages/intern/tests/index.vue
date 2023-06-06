<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <NuxtLink v-if="goingTestStore.test !== null" :to="{ name: 'intern-tests-current' }" class="link">
                    Текущий тест
                </NuxtLink>
            </template>
            <template #inputs>
                <ControlSearchInput v-model="search" />
            </template>
        </ControlPanel>
        <CommonContent>
            <CommonListViewTable :items="data!.items" with-id />
            <CommonLoadMore :response="data" @load-needed="loadMore" />
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const route = useRoute();

    const pageStore = usePageStore();

    const goingTestStore = useGoingTestStore();
    await goingTestStore.fetch();

    const search = ref<string | null | undefined>(getFirstQueryValue(route.query.search));

    const { data, loadMore } = await useListLoader({
        path: '/api/tests',
        method: 'get',
    });

    pageStore.fkInstancePathMap = {
        course: { name: 'intern-courses-id' },
        topic: {
            name: 'intern-my_courses-id-topics-topic_id',
            params: { id: '<<from-response>>' },
            response: data.value.items,
            routerToResponseParamsMap: {
                id: 'course_id',
            },
        },
    };
</script>
