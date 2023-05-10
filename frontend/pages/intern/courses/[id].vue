<template>
    <CommonContent>
        <div class="bg-white rounded-md px-6 py-4 shadow">
            <div class="text-lg border-b pb-3 mb-3">
                {{ data?.name }}
            </div>
            <div class="pb-3 mb-3 border-b">
                <div v-if="!data?.description" class="text-gray-600">Об этом курсе нет информации.</div>
                <div v-else class="whitespace-pre">
                    {{ data.description }}
                </div>
            </div>
            <div>
                <ControlButton>Записаться</ControlButton>
            </div>
        </div>
    </CommonContent>
</template>

<script setup lang="ts">
    const { $api } = useNuxtApp();
    const route = useRoute();
    usePageStore().name = 'Курсы';

    const { data } = await useAsyncData(() => {
        return $api({
            path: '/api/courses/{course_id}',
            method: 'get',
            params: {
                course_id: route.params.id as string,
            },
        });
    });
</script>
