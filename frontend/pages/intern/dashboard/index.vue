<template>
    <CommonContent class="grid gap-4">
        <InternDashboardStatistics class="col-span-4" />
        <InternDashboardAvailableCourses :courses="data?.[0].items!" />
    </CommonContent>
</template>

<script setup lang="ts">
    const { $api } = useNuxtApp();

    usePageStore().name = 'Личный кабинет';

    const { data } = await useAsyncData(() => {
        return Promise.all([
            $api({
                path: '/api/courses/',
                method: 'get',
                query: {
                    limit: 5,
                },
            }),
        ]);
    });
</script>
