<template>
    <CommonCard>
        <h2 class="text-lg mb-4">Полученные компетенции</h2>
        <p v-if="userStore.user?.competencies.length === 0" class="text-gray-600">
            У вас пока нет ни одной компетенции. Завершите хотя бы один
            <NuxtLink :to="{ name: 'intern-courses' }" class="link">курс</NuxtLink>
            и они появятся!
        </p>
        <div v-else>
            <p v-for="(competence, idx) in userStore.user!.competencies" :key="idx">
                {{ competence.name }}
            </p>
        </div>
    </CommonCard>
</template>

<script setup lang="ts">
    const userStore = useUserStore();
</script>
