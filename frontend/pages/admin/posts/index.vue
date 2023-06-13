<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonCreate />
            </template>
            <template #inputs>
                <ControlSearchInput v-model="search" />
            </template>
        </ControlPanel>
        <CommonContent>
            <CommonListViewTable
                :items="data!.items"
                :hide-fields="['subdivision_id']"
                route-name="admin-subdivisions-id-posts"
                link-param-name="post_id"
                :route-params-map="{ id: 'subdivision_id' }"
            />
            <CommonLoadMore :response="data" @load-needed="loadMore" />
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const { data, loadMore } = await useListLoader({ path: '/api/posts', method: 'get' });

    const route = useRoute();

    const search = ref<string | null | undefined>(getFirstQueryValue(route.query.search));
</script>
