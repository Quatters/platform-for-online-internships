<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
                <ControlButtonEdit />
                <ControlButtonDelete
                    path="/api/competencies/{competence_id}"
                    :params="{ competence_id: route.params.id as string}"
                />
            </template>
        </ControlPanel>
        <CommonContent>
            <CommonDetailViewCard :item="data!" />
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const { $api } = useNuxtApp();

    const route = useRoute();
    const pageStore = usePageStore();

    const { data } = await useAsyncData(() => {
        return $api({
            path: '/api/competencies/{competence_id}',
            method: 'get',
            params: {
                competence_id: route.params.id as string,
            },
        });
    });

    pageStore.fkInstancePathMap = {
        courses: {
            name: 'admin-courses-id',
        },
        posts: {
            name: 'admin-subdivisions-id-posts-post_id',
            params: {
                id: '<<from-response>>',
            },
            response: data.value?.posts,
            routerToResponseParamsMap: {
                id: 'subdivision_id',
            },
        },
    };
</script>
