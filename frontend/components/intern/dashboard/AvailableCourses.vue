<template>
    <CommonCard>
        <h2 class="text-lg mb-1">Рекомендуемые курсы</h2>
        <h2 class="mb-4">
            <span class="text-gray-700 me-1">для должности</span>
            <NuxtLink
                :to="{
                    name: 'intern-subdivisions-id-posts-post_id',
                    params: { id: post.subdivision_id, post_id: post.id },
                }"
                class="link"
            >
                {{ post.name }}
            </NuxtLink>
        </h2>
        <div class="overflow-y-auto max-h-[10rem]">
            <p v-for="(course, idx) in courses" :key="idx" class="mb-2">
                <NuxtLink :to="{ name: 'intern-courses-id', params: { id: course.id } }" class="link">
                    {{ course.name }}
                </NuxtLink>
            </p>
        </div>
        <div class="text-sm text-end mt-auto">
            <NuxtLink :to="{ name: 'intern-courses' }" class="link">Смотреть все</NuxtLink>
        </div>
    </CommonCard>
</template>

<script setup lang="ts">
    import { components } from '~/openapi';

    type Course = components['schemas']['Course'];

    defineProps<{
        courses: Course[];
        post: {
            id: number;
            name: string;
            subdivision_id: number;
        };
    }>();
</script>
