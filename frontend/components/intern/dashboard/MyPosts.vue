<template>
    <CommonCard>
        <h2 class="text-lg mb-4">Осваиваемые должности</h2>
        <p v-if="userStore.user?.posts.length === 0" class="text-gray-600">
            Вы пока не осваиваете ни одну должность. Начните с
            <NuxtLink :to="{ name: 'intern-subdivisions' }" class="link">выбора подразделения,</NuxtLink>
            чтобы начать обучаться.
        </p>
        <div v-else>
            <p v-for="(post, idx) in userStore.user!.posts" :key="idx">
                {{ post.name }}
            </p>
        </div>
    </CommonCard>
</template>

<script setup lang="ts">
    const userStore = useUserStore();
</script>
