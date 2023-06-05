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
                <ControlFormM2MField v-model="data.posts" path="/api/posts" class="mb-4" label="Должности" />
                <ControlFormM2MField v-model="data.courses" path="/api/courses/" class="mb-4" label="Курсы" />
            </ControlForm>
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    import { components } from '~/openapi';

    const { $api } = useNuxtApp();
    const { navigateBackwards } = useRouteUtils();

    type schema = components['schemas']['CreateCompetence'];

    const data = ref<schema>({
        name: '',
        posts: [],
        courses: [],
    });

    async function save() {
        await $api({
            path: '/api/competencies/',
            method: 'post',
            body: data.value,
        });
        return navigateBackwards();
    }
</script>
