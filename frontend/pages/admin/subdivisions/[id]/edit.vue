<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
            </template>
        </ControlPanel>
        <CommonContent>
            <ControlForm @submit="save">
                <ControlFormInput v-model="patchData.name" class="mb-4" label="Название" />
                <ControlFormTextArea v-model="patchData.description" class="mb-4" label="Описание" />
            </ControlForm>
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    import { components } from '~/openapi';

    usePageStore().name = 'Подразделения';

    const { $api } = useNuxtApp();
    const route = useRoute();
    const { navigateBackwards } = useRouteUtils();

    type schema = components['schemas']['PatchSubdivision'];

    const { data } = await useAsyncData(() => {
        return $api({
            path: '/api/subdivisions/{subdivision_id}',
            method: 'get',
            params: {
                subdivision_id: route.params.id as string,
            },
        });
    });

    const patchData = ref<schema>(data as schema);

    async function save() {
        await $api({
            path: '/api/subdivisions/{subdivision_id}',
            method: 'patch',
            params: {
                subdivision_id: route.params.id as string,
            },
            body: patchData.value,
        });
        return navigateBackwards();
    }
</script>
