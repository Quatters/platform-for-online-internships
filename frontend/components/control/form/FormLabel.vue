<template>
    <label :for="value" class="block mb-2 text-sm font-medium text-gray-900">
        <span>{{ value }}</span>
        <b v-if="required" class="ms-1 text-red-500">*</b>
    </label>
</template>

<script setup lang="ts">
    defineProps<{
        value: string;
        required?: boolean;
    }>();
</script>
