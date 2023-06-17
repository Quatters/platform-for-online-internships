<template>
    <div>
        <ControlPanel>
            <template #inputs>
                <ControlFormEnumField
                    v-model="status"
                    :enum-items="[
                        'in_progress',
                        'system_checking',
                        'timeout_failure',
                        'check_failure',
                        'partially_checked',
                        'checked',
                    ]"
                    class="w-64"
                />
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
    import { components } from '~/openapi';

    const route = useRoute();
    const router = useRouter();

    const pageStore = usePageStore();

    const goingTestStore = useTestStore();
    await goingTestStore.fetch();

    const search = ref<string | null | undefined>(getFirstQueryValue(route.query.search));
    const status = ref<components['schemas']['TestAttemptStatus']>();

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

    watch(status, value => {
        router.replace({
            ...route,
            query: {
                ...route.query,
                status: value ?? undefined,
            },
        });
    });
</script>
