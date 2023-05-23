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

    usePageStore().name = 'Подразделения';

    const { $api } = useNuxtApp();
    const { navigateBackwards } = useRouteUtils();

    type schema = components['schemas']['CreateSubdivision'];

    const data = ref<schema>({
        name: '',
        description: '',
    });

    async function save() {
        await $api({
            path: '/api/subdivisions/',
            method: 'post',
            body: data.value,
        });
        return navigateBackwards();
    }
</script>
