<template>
    <div v-if="item.type === 'text'">
        <div class="flex justify-between">
            <h2 class="text-xl font-medium mb-2">{{ item.name }}</h2>
            <slot />
        </div>
        <p>{{ item.value }}</p>
    </div>
    <div v-else>
        <div class="flex justify-center">
            <img v-if="item.type === 'image'" :src="item.value" class="w-full max-w-[50rem]" />
            <video v-else-if="item.type === 'video'" :src="item.value" controls />
            <iframe v-else-if="item.type === 'embedded'" :src="item.value" class="w-full min-h-[36rem]" />
        </div>
        <div class="flex justify-between mt-3">
            <span class="italic text-gray-500">{{ item.name }}</span>
            <slot />
        </div>
    </div>
</template>

<script setup lang="ts">
    import type { TopicResourceListItem } from '~/types';

    defineProps<{
        item: TopicResourceListItem;
    }>();
</script>
