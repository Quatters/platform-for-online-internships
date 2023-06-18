<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
                <ControlButtonCreate v-if="data?.status === 'unchecked'" page-name="grade" text="Оценить" />
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
            path: '/api/reviews/{review_id}',
            method: 'get',
            params: {
                review_id: route.params.id as string,
            },
        });
    });
</script>
