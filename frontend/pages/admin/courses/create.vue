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
                <ControlFormInput
                    v-model="data.pass_percent"
                    class="mb-4"
                    label="Процент для завершения"
                    type="number"
                    min="1"
                    max="100"
                    required
                />
                <ControlFormM2MField
                    v-model="data.competencies"
                    path="/api/competencies/"
                    class="mb-4"
                    label="Компетенции"
                />
                <ControlFormM2MField v-model="data.posts" path="/api/posts" class="mb-4" label="Должности" />
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
        competencies: [],
        posts: [],
        pass_percent: 86,
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
