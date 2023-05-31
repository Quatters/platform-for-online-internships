<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
            </template>
            <template #links>
                <NuxtLink :to="{ name: 'intern-subdivisions-id-posts', params: { id: route.params.id } }" class="link">
                    Должности
                </NuxtLink>
            </template>
        </ControlPanel>
        <CommonContent>
            <InternNameDescriptionCard :name="data!.name" :description="data?.description"></InternNameDescriptionCard>
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
