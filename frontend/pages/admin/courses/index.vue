<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonCreate />
            </template>
        </ControlPanel>
        <CommonContent>
            <CommonListViewTable :items="data!" />
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const { $api } = useNuxtApp();

    usePageStore().name = 'Курсы';

    const { data } = await useAsyncData(() =>
        $api({
            path: '/api/courses/',
            method: 'get',
        }),
    );
</script>
