<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
                <ControlButtonEdit />
                <ControlButtonDelete
                    path="/api/subdivisions/{subdivision_id}/posts/{post_id}"
                    :params="{ subdivision_id: route.params.id as string, post_id: route.params.post_id as string}"
                />
            </template>
        </ControlPanel>
        <CommonContent>
            <CommonDetailViewCard :item="data!" />
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const route = useRoute();

    const pageStore = usePageStore();
    pageStore.fkInstancePathMap = {
        courses: { name: 'admin-courses-id' },
    };

    const { $api } = useNuxtApp();

    const { data } = await useAsyncData(() => {
        return $api({
            path: '/api/subdivisions/{subdivision_id}/posts/{post_id}',
            method: 'get',
            params: { subdivision_id: route.params.id as string, post_id: route.params.post_id as string },
        });
    });
</script>
