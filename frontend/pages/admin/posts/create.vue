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
                <ControlFormInput v-model="data.description" class="mb-4" label="Описание" required />
                <ControlFormFkField
                    v-model="data.subdivision_id"
                    v-model:view-value="currentSubdivisionName"
                    path="/api/subdivisions/"
                    class="mb-4"
                    label="Подразделение"
                    required
                />
                <ControlFormM2MField v-model="data.courses" path="/api/courses/" class="mb-4" label="Курсы" />
                <ControlFormM2MField
                    v-model="data.competencies"
                    path="/api/competencies/"
                    class="mb-4"
                    label="Компетенции"
                />
            </ControlForm>
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    import { components } from '~/openapi';

    const { $api } = useNuxtApp();
    const { navigateBackwards } = useRouteUtils();

    type schema = components['schemas']['CreatePost'];

    const data = ref<schema>({
        name: '',
        description: '',
        courses: [],
        competencies: [],
        subdivision_id: undefined as unknown as number,
    });

    const currentSubdivisionName = ref<string>();

    async function save() {
        await $api({
            path: '/api/posts',
            method: 'post',
            body: data.value,
        });
        return navigateBackwards();
    }
</script>
