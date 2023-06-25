<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
                <ControlButtonEdit />
                <ControlButtonDelete
                    path="/api/courses/{course_id}"
                    :params="{ course_id: route.params.id as string}"
                />
            </template>
            <template #links>
                <NuxtLink :to="{ name: 'admin-courses-id-topics', params: { id: route.params.id } }" class="btn-link">
                    Темы
                </NuxtLink>
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
            path: '/api/courses/{course_id}',
            method: 'get',
            params: {
                course_id: route.params.id as string,
            },
        });
    });

    pageStore.fkInstancePathMap = {
        competencies: {
            name: 'admin-competencies-id',
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
