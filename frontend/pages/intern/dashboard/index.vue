<template>
    <CommonContent class="grid grid-rows-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <InternDashboardAvailableCourses
            v-for="(data, idx) in postCourses"
            :key="idx"
            :courses="data.items"
            :post="userStore.user!.posts[idx]"
            class="row-span-2 col-auto"
        />
        <InternDashboardAchievedCompetencies class="row-span-2 col-auto" />
        <InternDashboardMyPosts :posts="masteredPosts!" class="row-span-2 col-auto" />
    </CommonContent>
</template>

<script setup lang="ts">
    const { $api } = useNuxtApp();
    const userStore = useUserStore();

    await useAsyncData(() => {
        return userStore.fetchUser({ force: true });
    });

    const { data: masteredPosts } = await useAsyncData(() =>
        $api({
            path: '/api/mastered_posts',
            method: 'get',
        }),
    );

    const masteredPostIds = computed(() => {
        const posts = masteredPosts.value;
        if (!posts) {
            return [];
        }
        return posts.map(post => post.id);
    });

    const { data: postCourses } = await useAsyncData(() => {
        return Promise.all(
            userStore
                .user!.posts.filter(post => !masteredPostIds.value.includes(post.id))
                .map(post =>
                    $api({
                        path: '/api/courses/recommended',
                        method: 'get',
                        query: {
                            post_id: post.id,
                        },
                    }),
                ),
        );
    });
</script>
