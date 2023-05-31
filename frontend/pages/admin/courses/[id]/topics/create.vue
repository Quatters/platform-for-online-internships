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
                <ControlFormFkField
                    v-model="data.prev_topic_id"
                    v-model:view-value="prevTopicName"
                    path="/api/courses/{course_id}/topics/"
                    :params="{ course_id: route.params.id as string }"
                    class="mb-4"
                    label="Предыдущая тема"
                />
            </ControlForm>
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    import { components } from '~/openapi';

    const { $api } = useNuxtApp();
    const route = useRoute();
    const { navigateBackwards } = useRouteUtils();

    type schema = components['schemas']['CreateTopic'];

    const data = ref<schema>({
        name: '',
        description: '',
        prev_topic_id: undefined,
    });

    const prevTopicName = ref('');

    async function save() {
        await $api({
            path: '/api/courses/{course_id}/topics/',
            method: 'post',
            params: {
                course_id: route.params.id as string,
            },
            body: data.value,
        });
        return navigateBackwards();
    }
</script>
