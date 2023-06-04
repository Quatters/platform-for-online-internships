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
                <ControlFormTextArea v-model="patchData.value" class="mb-4" label="Значение" />
                <ControlFormFkField
                    v-model="patchData.prev_resource_id"
                    v-model:view-value="currentPrevResourceName"
                    nullable
                    path="/api/courses/{course_id}/topics/{topic_id}/resources/"
                    :params="{
                        course_id: route.params.id as string,
                        topic_id: route.params.topic_id as string,
                    }"
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

    const apiParams = {
        course_id: route.params.id as string,
        topic_id: route.params.topic_id as string,
        resource_id: route.params.resource_id as string,
    };

    type schema = components['schemas']['PatchTopicResource'];

    const { data } = await useAsyncData(() => {
        return $api({
            path: '/api/courses/{course_id}/topics/{topic_id}/resources/{resource_id}',
            method: 'get',
            params: apiParams,
        });
    });

    const { patchData } = usePatchDataInitializer<schema>(data, { fkFields: ['prev_resource'] });
    const currentPrevResourceName = ref(data.value?.prev_resource?.name);

    async function save() {
        await $api({
            path: '/api/courses/{course_id}/topics/{topic_id}/resources/{resource_id}',
            method: 'patch',
            params: apiParams,
            body: patchData.value,
        });
        return navigateBackwards();
    }
</script>
