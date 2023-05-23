<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
                <ControlButtonEdit />
                <ControlButtonDelete
                    path="/api/subdivisions/{subdivision_id}"
                    :params="{ subdivision_id: route.params.id as string}"
                />
            </template>
            <template #links>
                <NuxtLink :to="{ name: 'admin-subdivisions-id-posts', params: { id: route.params.id } }" class="link">
                    Должности
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
