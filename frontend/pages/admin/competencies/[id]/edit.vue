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
                <ControlFormM2MField v-model="patchData.posts" path="/api/posts" class="mb-4" label="Должности" />
                <ControlFormM2MField v-model="patchData.courses" path="/api/courses/" class="mb-4" label="Курсы" />
            </ControlForm>
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    import { components } from '~/openapi';

    const { $api } = useNuxtApp();
    const route = useRoute();
    const { navigateBackwards } = useRouteUtils();

    type schema = components['schemas']['PatchCompetence'];

    const { data } = await useAsyncData(() => {
        return $api({
            path: '/api/competencies/{competence_id}',
            method: 'get',
            params: {
                competence_id: route.params.id as string,
            },
        });
    });

    const { patchData } = usePatchDataInitializer<schema>(data, {
        m2mFields: ['posts', 'courses'],
    });

    async function save() {
        await $api({
            path: '/api/competencies/{competence_id}',
            method: 'patch',
            params: {
                competence_id: route.params.id as string,
            },
            body: patchData.value,
        });
        return navigateBackwards();
    }
</script>
