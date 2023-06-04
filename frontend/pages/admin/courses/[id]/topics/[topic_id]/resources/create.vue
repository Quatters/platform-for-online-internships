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
                <ControlFormTextArea v-model="data.value" class="mb-4" label="Значение" required />
                <ControlFormEnumField
                    v-model:model-value="data.type"
                    required
                    :enum-items="['text', 'image', 'video', 'embedded']"
                    class="mb-4"
                    label="Тип"
                />
                <ControlFormFkField
                    v-model="data.prev_resource_id"
                    v-model:view-value="prevResourceName"
                    path="/api/courses/{course_id}/topics/{topic_id}/resources/"
                    :params="{ course_id: route.params.id as string, topic_id: route.params.topic_id as string }"
                    class="mb-4"
                    label="Предыдущий ресурс"
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

    type schema = components['schemas']['CreateTopicResource'];

    const data = ref<schema>({
        name: '',
        type: 'text',
        value: '',
    });

    const prevResourceName = ref('');

    async function save() {
        await $api({
            path: '/api/courses/{course_id}/topics/{topic_id}/resources/',
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
