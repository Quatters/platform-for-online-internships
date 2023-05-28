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
                    v-model="patchData.prev_topic_id"
                    v-model:view-value="currentPrevTopicName"
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

    type schema = components['schemas']['PatchTopic'];

    const { data } = await useAsyncData(() => {
        return $api({
            path: '/api/courses/{course_id}/topics/{topic_id}',
            method: 'get',
            params: {
                course_id: route.params.id as string,
                topic_id: route.params.topic_id as string,
            },
        });
    });

    const { patchData } = usePatchDataInitializer<schema>(data, { fkFields: ['prev_topic'] });
    const currentPrevTopicName = ref(data.value?.prev_topic?.name);

    async function save() {
        await $api({
            path: '/api/courses/{course_id}/topics/{topic_id}',
            method: 'patch',
            params: {
                course_id: route.params.id as string,
                topic_id: route.params.topic_id as string,
            },
            body: patchData.value,
        });
        return navigateBackwards();
    }
</script>
