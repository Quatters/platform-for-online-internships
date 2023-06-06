<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButton variant="blue" @click="finish()">Завершить тест</ControlButton>
            </template>
            <template v-if="goingTestStore.test" #links>
                <span class="text-gray-500">
                    Начато: {{ new Date(goingTestStore.test.started_at).toLocaleString() }}
                </span>
            </template>
        </ControlPanel>
        <CommonContent>
            <CommonCard v-if="!goingTestStore.test">В настоящий момент вы не проходите тест.</CommonCard>
            <CommonCard v-else class="grid gap-5">
                <div>
                    <div class="flex justify-between border-b pb-3">
                        <div class="text-gray-500">Тест по теме</div>
                        <NuxtLink
                            :to="{
                                name: 'intern-my_courses-id-topics-topic_id',
                                params: {
                                    id: goingTestStore.test.topic.id,
                                    topic_id: goingTestStore.test.topic.course_id,
                                },
                            }"
                            class="link"
                        >
                            {{ goingTestStore.test.topic.name }}
                        </NuxtLink>
                    </div>
                </div>
                <div v-for="(task, idx) in goingTestStore.test?.tasks" :key="idx">
                    <h2 class="font-medium">{{ idx + 1 }}. {{ task.name }}</h2>
                    <div class="my-2">{{ task.description }}</div>
                    <InternTestAnswer
                        v-model="goingTestStore.answers[task.id]"
                        :possible-answers="task.possible_answers"
                        :type="task.task_type"
                        class="mb-3"
                    />
                </div>
            </CommonCard>
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const { $modal, $toast } = useNuxtApp();
    const i18n = useI18n();

    const goingTestStore = useGoingTestStore();
    await goingTestStore.fetch();

    function finish() {
        $modal.show({
            title: 'Подтвердите действие',
            body: 'Вы действительно хотите завершить тест?',
            type: 'danger',
            secondary: DEFAULT_SECONDARY_MODAL_BUTTON_OPTIONS,
            primary: {
                label: 'Завершить',
                theme: 'blue',
                action: async () => {
                    const data = await goingTestStore.finish();
                    $toast.show({
                        timeout: 4,
                        type: 'success',
                        title: i18n.t(data!.detail),
                    });
                    const testId = goingTestStore.test!.id;
                    goingTestStore.fetch({ force: true });
                    return navigateTo({
                        name: 'intern-tests-id',
                        params: { id: String(testId) },
                    });
                },
            },
        });
    }
</script>
