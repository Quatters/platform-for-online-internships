<template>
    <NuxtLayout>
        <NuxtPage />
    </NuxtLayout>
</template>

<script setup lang="ts"></script>

<style>
    .page-enter-active,
    .layout-enter-active,
    .page-leave-active,
    .layout-leave-active {
        transition: all 0.2s;
    }
    .page-enter-from,
    .layout-enter-from,
    .page-leave-to,
    .layout-leave-to {
        opacity: 0;
    }
</style>
