<template>
    <CommonContent>
        <NuxtLink
            v-for="(course, idx) in data?.items"
            :key="idx"
            :to="{ name: 'intern-my_courses-id', params: { id: course.course_id } }"
        >
            <div class="bg-white rounded-md px-6 py-4 mb-3 shadow">
                {{ course.course_name }}
            </div>
        </NuxtLink>
        <CommonLoadMore :response="data" @load-needed="loadMore" />
    </CommonContent>
</template>

<script setup lang="ts">
    usePageStore().name = 'Мои курсы';
    const userStore = useUserStore();
    const { data, loadMore } = await useListLoader({
        path: '/api/user/{user_id}/courses/',
        method: 'get',
        params: { user_id: userStore.user!.id },
    });
</script>
