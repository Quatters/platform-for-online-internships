<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
                <ControlButtonCreate page-name="assign" text="Прикрепить" />
            </template>
            <template #inputs>
                <ControlSearchInput v-model="search" />
            </template>
        </ControlPanel>
        <CommonContent>
            <TeacherInternWithStats v-for="intern in data.items" :key="intern.id" :intern="intern" />
            <CommonLoadMore :response="data" @load-needed="loadMore" />
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const route = useRoute();
    const userStore = useUserStore();

    const { data, loadMore } = await useListLoader({
        path: '/api/users/{teacher_id}/interns_with_stats',
        method: 'get',
        params: { teacher_id: userStore.user!.id },
    });

    const search = ref<string | null | undefined>(getFirstQueryValue(route.query.search));
</script>
