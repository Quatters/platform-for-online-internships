<template>
    <div class="bg-white shadow rounded-md px-6 py-4">
        <div class="text-lg mb-4">Доступные курсы</div>
        <div class="max-h-36 overflow-y-auto">
            <div v-for="(course, idx) in courses" :key="idx" class="mb-2">
                <NuxtLink :to="{ name: 'intern-courses-id', params: { id: course.id } }" class="link">
                    {{ course.name }}
                </NuxtLink>
            </div>
            <div class="flex justify-end text-sm">
                <NuxtLink :to="{ name: 'intern-courses' }" class="link">Смотреть все</NuxtLink>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { components } from '~/openapi';

    type Course = components['schemas']['Course'];

    defineProps<{
        courses: Course[];
    }>();
</script>
