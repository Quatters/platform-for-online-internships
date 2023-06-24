<template>
    <ControlButton @click="navigateToCreatePage()" variant="gray">{{ text }}</ControlButton>
</template>

<script setup lang="ts">
    const props = withDefaults(
        defineProps<{
            pageName?: string;
            text?: string;
        }>(),
        {
            pageName: 'create',
            text: 'Создать',
        },
    );

    const route = useRoute();

    function navigateToCreatePage() {
        return navigateTo({ name: `${String(route.name)}-${props.pageName}` });
    }
</script>
