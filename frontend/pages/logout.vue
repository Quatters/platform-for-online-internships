<template>
    <div></div>
</template>

<script setup lang="ts">
    definePageMeta({
        layout: 'clean',
    });

    const userStore = useUserStore();
    userStore.logout();
    navigateTo({ name: 'login' });
</script>
