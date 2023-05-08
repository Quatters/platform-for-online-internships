<template>
    <ControlButton variant="red" @click="deleteItem">Удалить</ControlButton>
</template>

<script setup lang="ts">
    import { APIPath } from '~/types';

    const { $api } = useNuxtApp();
    const { navigateBackwards } = useRouteUtils();

    const props = defineProps<{
        path: APIPath;
        params: Record<string, string | number>;
    }>();

    async function deleteItem() {
        await $api({
            path: props.path,
            // @ts-expect-error must support delete
            method: 'delete',
            params: props.params,
        });
        return navigateBackwards();
    }
</script>
