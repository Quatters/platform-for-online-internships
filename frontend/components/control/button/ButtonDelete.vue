<template>
    <ControlButton variant="red" @click="deleteItem">{{ text }}</ControlButton>
</template>

<script setup lang="ts">
    import { APIPath } from '~/types';

    const { $api, $modal } = useNuxtApp();
    const { navigateBackwards } = useRouteUtils();

    const props = withDefaults(
        defineProps<{
            path: APIPath;
            params: Record<string, string | number>;
            text?: string;
            confirmTitle?: string;
            confirmBody?: string | null;
        }>(),
        {
            text: 'Удалить',
            confirmTitle: DEFAULT_MODAL_TITLE,
            confirmBody: null,
        },
    );

    function deleteItem() {
        $modal.show({
            type: 'danger',
            title: props.confirmTitle,
            body: props.confirmBody ?? `Вы действительно хотите выполнить действие "${props.text}"?`,
            primary: {
                label: props.text,
                action: async () => {
                    await $api({
                        path: props.path,
                        // @ts-expect-error must support delete
                        method: 'delete',
                        params: props.params,
                    });
                    return navigateBackwards();
                },
                theme: 'red',
            },
            secondary: {
                label: 'Отмена',
                action: noop,
                theme: 'text',
            },
        });
    }
</script>
