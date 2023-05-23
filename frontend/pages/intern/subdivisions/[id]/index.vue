<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
            </template>
            <template #links>
                <ControlNestedLink :to="{ name: 'intern-subdivisions-id-posts', params: { id: route.params.id } }">
                    Должности
                </ControlNestedLink>
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
            path: '/api/subdivisions/{subdivision_id}',
            method: 'get',
            params: {
                subdivision_id: route.params.id as string,
            },
        });
    });
</script>
