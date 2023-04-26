<template>
    <CommonSidebar :sidebar-items="sidebarItems" />
    <slot></slot>
</template>

<script setup lang="ts">
    const sidebarItems = [
        { link: '/', title: 'Стажёры' },
        { link: '/tasks', title: 'Задания' },
    ];
</script>
