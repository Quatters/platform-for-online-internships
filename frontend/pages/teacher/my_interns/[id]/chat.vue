<template>
    <CommonContent>
        <ChatComponent :recipient-id="Number(route.params.id)" />
    </CommonContent>
</template>

<script setup lang="ts">
    const route = useRoute();
</script>
