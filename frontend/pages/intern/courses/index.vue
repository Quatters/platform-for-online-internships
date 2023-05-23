<template>
    <div>
        <ControlPanel>
            <template #inputs>
                <ControlSearchInput v-model="search" />
            </template>
        </ControlPanel>
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
    </div>
</template>

<script setup lang="ts">
    const route = useRoute();

    const search = ref<string | null | undefined>(getFirstQueryValue(route.query.search));

    const { data, loadMore } = await useListLoader({
        path: '/api/courses/',
        method: 'get',
    });
</script>
