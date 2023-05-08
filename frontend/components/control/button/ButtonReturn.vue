<template>
    <ControlButton variant="gray" @click="() => navigateBackwards()">Назад</ControlButton>
</template>

<script setup lang="ts">
    const { navigateBackwards } = useRouteUtils();
</script>
