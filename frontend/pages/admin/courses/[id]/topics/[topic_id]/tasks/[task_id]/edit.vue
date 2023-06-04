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
                <ControlFormFkField
                    v-model="patchData.prev_task_id"
                    v-model:view-value="currentPrevTaskName"
                    path="/api/courses/{course_id}/topics/{topic_id}/tasks/"
                    :params="{
                        course_id: route.params.id as string,
                        topic_id: route.params.topic_id as string,
                    }"
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

    const apiParams = {
        course_id: route.params.id as string,
        topic_id: route.params.topic_id as string,
        task_id: route.params.task_id as string,
    };

    type schema = components['schemas']['PatchTask'];

    const { data } = await useAsyncData(() => {
        return $api({
            path: '/api/courses/{course_id}/topics/{topic_id}/tasks/{task_id}',
            method: 'get',
            params: apiParams,
        });
    });

    const { patchData } = usePatchDataInitializer<schema>(data, { fkFields: ['prev_task'] });
    const currentPrevTaskName = ref(data.value?.prev_task?.name);

    async function save() {
        await $api({
            path: '/api/courses/{course_id}/topics/{topic_id}/tasks/{task_id}',
            method: 'patch',
            params: apiParams,
            body: patchData.value,
        });
        return navigateBackwards();
    }
</script>
