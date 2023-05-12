<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
                <ControlButtonDelete
                    text="Покинуть курс"
                    path="/api/user/{user_id}/courses/{course_id}"
                    :params="myCourseParams"
                    :confirm-body="leaveCourseConfirmBody"
                />
            </template>
        </ControlPanel>
        <CommonContent>
            <CommonCard>
                <div class="text-lg border-b pb-3 mb-3">
                    {{ course?.course_name }}
                </div>
                <div class="pb-3 mb-3 border-b">
                    <div v-if="!course?.course_description" class="text-gray-600">Об этом курсе нет информации.</div>
                    <div v-else class="whitespace-pre">
                        {{ course.course_description }}
                    </div>
                </div>
                <div class="text-gray-600">
                    <div>Дата поступления: {{ new Date(course!.admission_date).toLocaleDateString() }}</div>
                    <div>Прогресс обучения: {{ course!.progress }}%</div>
                </div>
            </CommonCard>
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const { $api } = useNuxtApp();
    const userStore = useUserStore();
    const route = useRoute();

    usePageStore().name = 'Мои курсы';

    const myCourseParams = {
        user_id: userStore.user!.id,
        course_id: route.params.id as string,
    };

    const { data: course } = await useAsyncData(() => {
        return $api({
            path: '/api/user/{user_id}/courses/{course_id}',
            method: 'get',
            params: myCourseParams,
        });
    });

    const leaveCourseConfirmBody = computed(() => {
        return `Вы действительно хотите покинуть курс "${course.value?.course_name}"?`;
    });
</script>
