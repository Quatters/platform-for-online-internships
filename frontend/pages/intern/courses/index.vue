<template>
    <CommonContent>
        <div v-for="course in data?.items" :key="course.id">
            <NuxtLink v-if="course.id" :to="{ name: 'intern-courses-id', params: { id: course.id } }">
                <div class="bg-white rounded-md px-6 py-4 mb-3 shadow">
                    {{ course.name }}
                </div>
            </NuxtLink>
        </div>
        <CommonLoadMore :response="data" @load-needed="loadMore" />
    </CommonContent>
</template>

<script setup lang="ts">
    usePageStore().name = 'Курсы';
    const { data, loadMore } = await useListLoader({ path: '/api/courses/', method: 'get' });
</script>
