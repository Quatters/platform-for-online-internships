<template>
    <label :for="value" class="block text-gray-700 font-medium mb-2">
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
