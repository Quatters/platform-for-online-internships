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
        </ControlPanel>
        <CommonContent>
            <CommonDetailViewCard :item="data!" />
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const { $api } = useNuxtApp();

    const route = useRoute();

    const { data } = await useAsyncData(() => {
        return $api({
            path: '/api/courses/{course_id}',
            method: 'get',
            params: {
                course_id: route.params.id as string,
            },
        });
    });
</script>
