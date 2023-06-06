<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
            </template>
        </ControlPanel>
        <CommonContent>
            <CommonCard>
                <div class="pb-3 mb-3 border-b text-lg">Тест {{ data?.id }}</div>
                <label class="block my-2">
                    <span class="inline-block font-medium">Баллы</span>
                    <FieldString field-name="score" :value="data?.score" class="block" />
                </label>
                <label class="block my-2">
                    <span class="inline-block font-medium">Максимальный балл</span>
                    <FieldString field-name="max_score" :value="data?.max_score" class="block" />
                </label>
                <label class="block my-2">
                    <span class="inline-block font-medium">Начат</span>
                    <div>{{ new Date(data!.started_at).toLocaleString() }}</div>
                </label>
                <label class="block my-2">
                    <span class="inline-block font-medium">Закончен</span>
                    <div>{{ new Date(data!.finished_at).toLocaleString() }}</div>
                </label>
                <label class="block my-2">
                    <span class="inline-block font-medium">Статус</span>
                    <FieldString field-name="status" :value="data?.status" class="block" />
                </label>
                <label class="block my-2">
                    <span class="inline-block font-medium">Курс</span>
                    <FieldObject field-name="course" :value="data?.course" class="block" />
                </label>
                <label class="block my-2">
                    <span class="inline-block font-medium">Тема</span>
                    <FieldObject field-name="topic" :value="data?.topic" class="block" />
                </label>
            </CommonCard>
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const { $api } = useNuxtApp();
    const pageStore = usePageStore();

    const route = useRoute();

    const { data } = await useAsyncData(() => {
        return $api({
            path: '/api/tests/{test_id}',
            method: 'get',
            params: {
                test_id: route.params.id as string,
            },
        });
    });

    pageStore.fkInstancePathMap = {
        course: { name: 'intern-courses-id' },
        topic: {
            name: 'intern-my_courses-id-topics-topic_id',
            params: { id: '<<from-response>>' },
            response: data.value?.topic,
            routerToResponseParamsMap: {
                id: 'course_id',
            },
        },
    };
</script>
