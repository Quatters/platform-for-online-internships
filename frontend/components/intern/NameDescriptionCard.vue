<template>
    <CommonCard>
        <div class="text-lg border-b pb-3 mb-3">
            {{ name }}
        </div>
        <div class="pb-3">
            <div v-if="!description" class="text-gray-600">Нет информации.</div>
            <div v-else class="whitespace-pre-wrap">
                {{ description }}
            </div>
        </div>
        <slot name="additional-content" />
    </CommonCard>
</template>

<script setup lang="ts">
    defineProps<{
        name: string;
        description?: string;
    }>();
</script>
