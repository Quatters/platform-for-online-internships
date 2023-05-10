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

    type schema = components['schemas']['backend__api__schemas__courses__CreateCourse'];

    const data = ref<schema>({
        name: '',
        description: '',
    });

    async function save() {
        nameError.value = '';
        try {
            await $api({
                path: '/api/courses/',
                method: 'post',
                body: data.value,
            });
            return navigateBackwards();
        } catch (e) {
            console.error(e);

            if (e instanceof FetchError) {
                if (e.data?.code === 'integrity_error') {
                    nameError.value = 'Курс с таким названием уже существует.';
                }
            }
        }
    }
</script>
