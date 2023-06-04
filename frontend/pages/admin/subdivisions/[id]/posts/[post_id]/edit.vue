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
                <ControlFormM2MField v-model="patchData.courses" path="/api/courses/" label="Курсы" class="mb-3" />
            </ControlForm>
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    import { components } from '~/openapi';

    const { $api } = useNuxtApp();
    const route = useRoute();
    const { navigateBackwards } = useRouteUtils();

    type schema = components['schemas']['PatchSubdivisionPost'];

    const { data } = await useAsyncData(() => {
        return $api({
            path: '/api/subdivisions/{subdivision_id}/posts/{post_id}',
            method: 'get',
            params: {
                subdivision_id: route.params.id as string,
                post_id: route.params.post_id as string,
            },
        });
    });

    const { patchData } = usePatchDataInitializer<schema>(data, { m2mFields: ['courses'] });

    async function save() {
        await $api({
            path: '/api/subdivisions/{subdivision_id}/posts/{post_id}',
            method: 'patch',
            params: {
                subdivision_id: route.params.id as string,
                post_id: route.params.post_id as string,
            },
            body: patchData.value,
        });
        return navigateBackwards();
    }
</script>
