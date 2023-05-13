<template>
    <div
        class="animate-spin inline-block border-[3px] border-current border-t-transparent rounded-full"
        :class="computedClasses"
        role="status"
        aria-label="loading"
    >
        <span class="sr-only">Загрузка...</span>
    </div>
</template>

<script setup lang="ts">
    const props = withDefaults(
        defineProps<{
            size?: number;
        }>(),
        {
            size: 6,
        },
    );

    const computedClasses = computed(() => {
        return `w-${props.size} h-${props.size}`;
    });
</script>
