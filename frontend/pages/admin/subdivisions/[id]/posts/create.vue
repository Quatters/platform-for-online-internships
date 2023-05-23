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
                <ControlFormM2MField v-model="data.courses" path="/api/courses/" label="Курсы" class="mb-3" />
            </ControlForm>
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    import { components } from '~/openapi';

    usePageStore().name = 'Должности';

    const { $api } = useNuxtApp();
    const { navigateBackwards } = useRouteUtils();
    const route = useRoute();

    type schema = components['schemas']['CreateSubdivisionPost'];

    const data = ref<schema>({
        name: '',
        description: '',
        courses: [],
    });

    async function save() {
        await $api({
            path: '/api/subdivisions/{subdivision_id}/posts',
            params: {
                subdivision_id: route.params.id as string,
            },
            method: 'post',
            body: data.value,
        });
        return navigateBackwards();
    }
</script>
