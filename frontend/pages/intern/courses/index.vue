<template>
    <CommonContent>
        <NuxtLink
            v-for="(course, idx) in data?.items"
            :key="idx"
            :to="{ name: 'intern-courses-id', params: { id: course.id } }"
        >
            <div class="bg-white rounded-md px-6 py-4 mb-3 shadow">
                {{ course.name }}
            </div>
        </NuxtLink>
        <CommonLoadMore @load-needed="loadMore" :response="data" />
    </CommonContent>
</template>

<script setup lang="ts">
    usePageStore().name = 'Курсы';
    const { data, loadMore } = await useAsyncDataWithLoader({ path: '/api/courses/', method: 'get' });
</script>
