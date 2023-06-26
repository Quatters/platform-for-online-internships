<template>
    <CommonContent class="grid grid-rows-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <!-- <InternDashboardStatistics class="col-span-auto row-span-1 md:col-span-2 xl:col-span-1" /> -->
        <InternDashboardAvailableCourses :courses="data?.[0].items!" class="row-span-2 col-auto" />
        <InternDashboardAchievedCompetencies class="row-span-2 col-auto" />
        <InternDashboardMyPosts class="row-span-2 col-auto" />
    </CommonContent>
</template>

<script setup lang="ts">
    const { $api } = useNuxtApp();
    const userStore = useUserStore();

    const { data } = await useAsyncData(() => {
        return Promise.all([
            $api({
                path: '/api/courses/',
                method: 'get',
                query: {
                    limit: 5,
                },
            }),
            userStore.fetchUser({ force: true }),
        ]);
    });
</script>
