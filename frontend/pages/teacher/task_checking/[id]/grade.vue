<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
            </template>
        </ControlPanel>
        <CommonContent>
            <ControlForm @submit="save">
                <ControlFormInput
                    v-model="data.score"
                    class="mb-4"
                    label="Баллы"
                    required
                    min="0"
                    max="5"
                    type="number"
                />
                <ControlFormTextArea v-model="data.review" class="mb-4" label="Комментарий" />
            </ControlForm>
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    import { components } from '~/openapi';

    const { $api, $modal } = useNuxtApp();
    const { navigateBackwards } = useRouteUtils();
    const route = useRoute();

    type schema = components['schemas']['FinishReview'];

    const data = ref<schema>({
        review: undefined,
        score: 0,
    });

    function save() {
        $modal.show({
            title: 'Подтвердите действие',
            type: 'warning',
            body: 'Сохранить оценку? В будущем ее нельзя будет изменить.',
            secondary: DEFAULT_SECONDARY_MODAL_BUTTON_OPTIONS,
            primary: {
                theme: 'blue',
                label: 'Сохранить',
                action: async () => {
                    await $api({
                        path: '/api/reviews/{review_id}',
                        method: 'put',
                        body: data.value,
                        params: {
                            review_id: route.params.id as string,
                        },
                    });
                    return navigateBackwards();
                },
            },
        });
    }
</script>
