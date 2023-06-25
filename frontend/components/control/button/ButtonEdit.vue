<template>
    <ControlButton @click="navigateToEditPage()">Редактировать</ControlButton>
</template>

<script setup lang="ts">
    const route = useRoute();

    function navigateToEditPage() {
        return navigateTo({ name: `${String(route.name)}-edit` });
    }
</script>
