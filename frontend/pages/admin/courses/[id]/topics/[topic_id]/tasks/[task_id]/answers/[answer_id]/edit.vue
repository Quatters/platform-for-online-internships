<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
            </template>
        </ControlPanel>
        <CommonContent>
            <ControlForm @submit="save">
                <ControlFormInput v-model="patchData.value" class="mb-4" label="Значение" />
                <ControlFormBooleanField v-model="patchData.is_correct" class="mb-4" label="Правильный ответ" />
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
        answer_id: route.params.answer_id as string,
    };

    type schema = components['schemas']['PatchAnswer'];

    const { data } = await useAsyncData(() => {
        return $api({
            path: '/api/courses/{course_id}/topics/{topic_id}/tasks/{task_id}/answers/{answer_id}',
            method: 'get',
            params: apiParams,
        });
    });

    const { patchData } = usePatchDataInitializer<schema>(data);

    async function save() {
        await $api({
            path: '/api/courses/{course_id}/topics/{topic_id}/tasks/{task_id}/answers/{answer_id}',
            method: 'patch',
            params: apiParams,
            body: patchData.value,
        });
        return navigateBackwards();
    }
</script>
