<template>
    <div class="text-white">
        <div class="text-2xl font-bold">{{ value }}</div>
        <div class="">{{ text }}</div>
    </div>
</template>

<script setup lang="ts">
    defineProps<{
        text: string;
        value: string | number;
    }>();
</script>
