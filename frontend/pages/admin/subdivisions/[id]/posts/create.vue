<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
            </template>
        </ControlPanel>
        <CommonContent>
            <ControlForm @submit="save">
                <ControlFormInput v-model="data.name" :error="nameError" class="mb-4" label="Название" required />
                <ControlFormTextArea v-model="data.description" class="mb-4" label="Описание" required />
            </ControlForm>
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    import { FetchError } from 'ofetch';
    import { components } from '~/openapi';

    const { $api } = useNuxtApp();
    const { navigateBackwards } = useRouteUtils();
    const nameError = ref('');
    const route = useRoute();

    type schema = components['schemas']['CreateSubdivisionPost'];

    const data = ref<schema>({
        name: '',
        description: '',
    });

    async function save() {
        nameError.value = '';
        try {
            await $api({
                path: '/api/subdivisions/{subdivision_id}/posts',
                params: {
                    subdivision_id: route.params.id as string,
                },
                method: 'post',
                body: data.value,
            });
            return navigateBackwards();
        } catch (e) {
            console.error(e);

            if (e instanceof FetchError) {
                if (e.data?.code === 'integrity_error') {
                    nameError.value = 'Должность с таким названием уже существует.';
                }
            }
        }
    }
</script>
