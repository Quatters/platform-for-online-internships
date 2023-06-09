<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
                <ControlButtonEdit />
                <ControlButtonDelete path="/api/users/{user_id}" :params="{ user_id: route.params.id as string}" />
            </template>
        </ControlPanel>
        <CommonContent>
            <CommonDetailViewCard :item="data!" :hide-fields="data!.is_admin ? ['posts'] : []" />
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const { $api } = useNuxtApp();

    const route = useRoute();

    const pageStore = usePageStore();
    pageStore.fkInstancePathMap = {
        posts: { name: 'admin-subdivisions-id-posts-post_id', params: { id: route.params.id } },
    };

    const { data } = await useAsyncData(() => {
        return $api({
            path: '/api/users/{user_id}',
            method: 'get',
            params: {
                user_id: route.params.id as string,
            },
        });
    });
</script>
