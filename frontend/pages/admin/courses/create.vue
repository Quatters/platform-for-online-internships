<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
            </template>
        </ControlPanel>
        <CommonContent>
            <ControlForm @submit="save">
                <ControlFormInput v-model="data.name" class="mb-4" label="Название" required />
                <ControlFormTextArea v-model="data.description" class="mb-4" label="Описание" required />
            </ControlForm>
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    import { components } from '~/openapi';

    const { $api } = useNuxtApp();
    const { navigateBackwards } = useRouteUtils();

    type schema = components['schemas']['backend__api__schemas__courses__CreateCourse'];

    const data = ref<schema>({
        name: '',
        description: '',
    });

    async function save() {
        await $api({
            path: '/api/courses/',
            method: 'post',
            body: data.value,
        });
        return navigateBackwards();
    }
</script>
