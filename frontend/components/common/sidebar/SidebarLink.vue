<template>
    <NuxtLink :to="to" class="flex flex-row items-center text-blue-900 mx-3 mt-2 py-1 ps-7 sidebar-link">
        <div
            class="w-5 h-5 rounded-full circle transition-all duration-100"
            :class="matchRoute() ? '!bg-blue-800' : 'bg-blue-200'"
        />
        <div class="mx-5 title transition-all duration-100">{{ title }}</div>
    </NuxtLink>
</template>

<script setup lang="ts">
    import { RouteLocationRaw } from 'vue-router';

    const props = defineProps<{
        to: RouteLocationRaw;
        title: string;
    }>();

    const router = useRouter();
    const route = useRoute();

    function matchRoute() {
        return route.path.startsWith(router.resolve(props.to).path);
    }
</script>

<style scoped lang="scss">
    .sidebar-link:hover > .title {
        @apply text-blue-700;
    }

    .sidebar-link:hover > .circle {
        @apply bg-blue-400;
    }
</style>
