<template>
    <CommonContent>
        <ChatComponent :recipient-id="userStore.user!.teacher!.id" />
    </CommonContent>
</template>

<script setup lang="ts">
    const userStore = useUserStore();

    if (!userStore.user?.teacher) {
        navigateTo('/');
    }
</script>
