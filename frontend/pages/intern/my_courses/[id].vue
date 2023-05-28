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
                    :success-title="successTitle"
                />
            </template>
        </ControlPanel>
        <CommonContent>
            <InternNameDescriptionCard :name="course!.course_name" :description="course?.course_description">
                <template #additional-content>
                    <label class="block mb-6 w-full">
                        <span class="inline-block mb-1">Должности, осваиваемые этим курсом</span>
                        <FieldArray :value="course!.posts" field-name="posts" />
                    </label>
                    <div class="text-gray-600">
                        <div>Дата поступления: {{ new Date(course!.admission_date).toLocaleDateString() }}</div>
                        <div>Прогресс обучения: {{ course!.progress }}%</div>
                    </div>
                </template>
            </InternNameDescriptionCard>
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const { $api } = useNuxtApp();
    const userStore = useUserStore();
    const route = useRoute();
    const pageStore = usePageStore();

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

    pageStore.fkInstancePathMap = {
        posts: {
            name: 'intern-subdivisions-id-posts-post_id',
            params: {
                id: '<<from-response>>',
            },
            response: course.value?.posts,
            routerToResponseParamsMap: {
                id: 'subdivision_id',
            },
        },
    };

    const leaveCourseConfirmBody = computed(() => {
        return `Вы действительно хотите покинуть курс "${course.value?.course_name}"?`;
    });

    const successTitle = computed(() => {
        return `Вы покинули курс "${course.value?.course_name}"`;
    });
</script>
