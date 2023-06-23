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
                <ControlFormInput
                    v-model="patchData.pass_percent"
                    class="mb-4"
                    label="Процент для завершения"
                    type="number"
                    min="1"
                    max="100"
                />
                <ControlFormM2MField
                    v-model="patchData.competencies"
                    path="/api/competencies/"
                    class="mb-4"
                    label="Компетенции"
                />
                <ControlFormM2MField v-model="patchData.posts" path="/api/posts" class="mb-4" label="Должности" />
            </ControlForm>
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    import { components } from '~/openapi';

    const { $api } = useNuxtApp();
    const route = useRoute();
    const { navigateBackwards } = useRouteUtils();

    type schema = components['schemas']['PatchCourse'];

    const { data } = await useAsyncData(() => {
        return $api({
            path: '/api/courses/{course_id}',
            method: 'get',
            params: {
                course_id: route.params.id as string,
            },
        });
    });

    const { patchData } = usePatchDataInitializer<schema>(data, {
        m2mFields: ['competencies', 'posts'],
    });

    async function save() {
        await $api({
            path: '/api/courses/{course_id}',
            method: 'patch',
            params: {
                course_id: route.params.id as string,
            },
            body: patchData.value,
        });
        return navigateBackwards();
    }
</script>
