<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
            </template>
        </ControlPanel>
        <CommonContent>
            <ControlForm @submit="save">
                <ControlFormInput v-model="data.value" class="mb-4" label="Значение" required />
                <ControlFormBooleanField v-model="data.is_correct" class="mb-4" required label="Правильный ответ" />
            </ControlForm>
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    import { components } from '~/openapi';

    const { $api } = useNuxtApp();
    const route = useRoute();
    const { navigateBackwards } = useRouteUtils();

    const apiParams = {
        course_id: route.params.id as string,
        topic_id: route.params.topic_id as string,
        task_id: route.params.task_id as string,
    };

    type schema = components['schemas']['CreateAnswer'];

    const data = ref<schema>({
        is_correct: false,
        value: '',
    });

    async function save() {
        await $api({
            path: '/api/courses/{course_id}/topics/{topic_id}/tasks/{task_id}/answers/',
            method: 'post',
            params: apiParams,
            body: data.value,
        });
        return navigateBackwards();
    }
</script>
