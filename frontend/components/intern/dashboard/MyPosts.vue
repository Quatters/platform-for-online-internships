<template>
    <CommonCard>
        <h2 class="text-lg mb-4">Освоенные должности</h2>
        <p v-if="!posts?.length" class="text-gray-600">
            Вы пока не освоили ни одну должность. Завершайте курсы, зарабатывайте компетенции и у вас все получится!
        </p>
        <div v-else class="max-h-[10rem] overflow-y-auto">
            <p v-for="(post, idx) in posts" :key="idx">
                <NuxtLink
                    :to="{
                        name: 'intern-subdivisions-id-posts-post_id',
                        params: { id: post.subdivision_id, post_id: post.id },
                    }"
                    class="link"
                >
                    {{ post.name }}
                </NuxtLink>
            </p>
        </div>
    </CommonCard>
</template>

<script setup lang="ts">
    defineProps<{
        posts: {
            id: number;
            name: string;
            subdivision_id: number;
        }[];
    }>();
</script>
