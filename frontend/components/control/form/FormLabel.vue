<template>
    <label :for="value" class="block text-gray-700 font-medium mb-2">
        {{ value }}
        <b v-if="required" class="text-red-500">*</b>
    </label>
</template>

<script setup lang="ts">
    defineProps<{
        value: string;
        required?: boolean;
    }>();
</script>
