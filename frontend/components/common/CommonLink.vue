<template>
    <!-- eslint-disable-next-line vue/no-parsing-error -->
    <NuxtLink :to="to" class="link" :class="class">{{ text }}</NuxtLink>
</template>

<script setup lang="ts">
    import { RouteLocationRaw } from 'vue-router';

    withDefaults(
        defineProps<{
            to: RouteLocationRaw;
            text: string;
            class?: string;
        }>(),
        {
            class: '',
        },
    );
</script>
