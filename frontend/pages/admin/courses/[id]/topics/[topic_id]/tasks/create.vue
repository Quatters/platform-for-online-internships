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
                <ControlFormEnumField
                    v-model:model-value="data.task_type"
                    required
                    :enum-items="['single', 'multiple', 'text']"
                    class="mb-4"
                    label="Тип задания"
                />
                <ControlFormFkField
                    v-model="data.prev_task_id"
                    v-model:view-value="prevTaskName"
                    path="/api/courses/{course_id}/topics/{topic_id}/tasks/"
                    :params="{ course_id: route.params.id as string, topic_id: route.params.topic_id as string }"
                    class="mb-4"
                    label="Предыдущее задание"
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

    type schema = components['schemas']['CreateTask'];

    const data = ref<schema>({
        name: '',
        description: '',
        prev_task_id: undefined,
        task_type: 'single',
    });

    const prevTaskName = ref('');

    async function save() {
        await $api({
            path: '/api/courses/{course_id}/topics/{topic_id}/tasks/',
            method: 'post',
            params: {
                course_id: route.params.id as string,
                topic_id: route.params.topic_id as string,
            },
            body: data.value,
        });
        return navigateBackwards();
    }
</script>
