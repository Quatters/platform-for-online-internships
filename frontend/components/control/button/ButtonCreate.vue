<template>
    <ControlButton @click="() => navigateTo({ name: `${String($route.name)}-${pageName}` })">{{ text }}</ControlButton>
</template>

<script setup lang="ts">
    withDefaults(
        defineProps<{
            pageName?: string;
            text?: string;
        }>(),
        {
            pageName: 'create',
            text: 'Создать',
        },
    );
</script>
