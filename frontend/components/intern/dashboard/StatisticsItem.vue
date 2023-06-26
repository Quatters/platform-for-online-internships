<template>
    <div class="text-white">
        <div class="text-lg sm:text-2xl font-bold">{{ value }}</div>
        <div class="text-sm sm:text-base">{{ text }}</div>
    </div>
</template>

<script setup lang="ts">
    defineProps<{
        text: string;
        value: string | number;
    }>();
</script>
