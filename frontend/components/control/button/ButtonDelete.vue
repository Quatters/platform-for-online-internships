<template>
    <ControlButton variant="red" @click="deleteItem">{{ text }}</ControlButton>
</template>

<script setup lang="ts">
    import { APIPath } from '~/types';

    const { $api, $modal, $toast } = useNuxtApp();
    const { navigateBackwards } = useRouteUtils();

    const props = withDefaults(
        defineProps<{
            path: APIPath;
            params: Record<string, string | number>;
            text?: string;
            confirmTitle?: string;
            confirmBody?: string | null;
            successTitle?: string | null;
            successMessage?: string;
        }>(),
        {
            text: 'Удалить',
            confirmTitle: DEFAULT_MODAL_TITLE,
            confirmBody: null,
            successTitle: null,
            successMessage: undefined,
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
                    $toast.show({
                        title: props.successTitle ?? `Действие "${props.text}" успешно выполнено`,
                        message: props.successMessage,
                        type: 'info',
                        timeout: 4,
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
