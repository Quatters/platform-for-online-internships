<template>
    <div>
        <ControlPanel>
            <template #inputs>
                <ControlFormEnumField v-model="status" :enum-items="['checked', 'unchecked']" class="w-44" />
                <ControlSearchInput v-model="search" />
            </template>
        </ControlPanel>
        <CommonContent>
            <CommonListViewTable :items="data!.items" />
            <CommonLoadMore :response="data" @load-needed="loadMore" />
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const route = useRoute();
    const router = useRouter();

    const { data, loadMore } = await useListLoader({
        path: '/api/reviews/',
        method: 'get',
    });

    const search = ref<string | null | undefined>(getFirstQueryValue(route.query.search));
    const status = ref<string>();

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
