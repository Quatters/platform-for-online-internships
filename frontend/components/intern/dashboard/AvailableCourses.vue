<template>
    <CommonCard class="relative">
        <h2 class="text-lg mb-4">Доступные курсы</h2>
        <div class="overflow-y-auto">
            <p v-for="(course, idx) in courses" :key="idx" class="mb-2">
                <NuxtLink :to="{ name: 'intern-courses-id', params: { id: course.id } }" class="link">
                    {{ course.name }}
                </NuxtLink>
            </p>
        </div>
        <div class="absolute bottom-0 right-0 p-[inherit] text-sm">
            <NuxtLink :to="{ name: 'intern-courses' }" class="link">Смотреть все</NuxtLink>
        </div>
    </CommonCard>
</template>

<script setup lang="ts">
    import { components } from '~/openapi';

    type Course = components['schemas']['Course'];

    defineProps<{
        courses: Course[];
    }>();
</script>
