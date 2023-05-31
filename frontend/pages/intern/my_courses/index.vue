<template>
    <div>
        <ControlPanel>
            <template #inputs>
                <ControlSearchInput v-model="search" />
            </template>
        </ControlPanel>
        <CommonContent>
            <CommonListViewTable
                :items="data!.items"
                :hide-fields="['user_id', 'course_id', 'admission_date']"
                api-value-field-name="course_id"
            />
            <CommonLoadMore :response="data" @load-needed="loadMore" />
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const userStore = useUserStore();
    const route = useRoute();

    const search = ref<string | null | undefined>(getFirstQueryValue(route.query.search));

    const { data, loadMore } = await useListLoader({
        path: '/api/user/{user_id}/courses/',
        method: 'get',
        params: { user_id: userStore.user!.id },
    });
</script>
