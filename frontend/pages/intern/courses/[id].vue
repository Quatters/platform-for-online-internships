<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
            </template>
        </ControlPanel>
        <CommonContent>
            <InternNameDescriptionCard :name="courseName" :description="courseDescription">
                <template #additional-content>
                    <label class="block mb-6 w-full">
                        <span class="inline-block mb-1">Должности, осваиваемые этим курсом</span>
                        <FieldArray :value="course!.posts" field-name="posts" />
                    </label>
                    <label class="block mb-6 w-full">
                        <span class="inline-block mb-1">Компетенции, осваиваемые этим курсом</span>
                        <FieldArray :value="course!.competencies" field-name="competencies" />
                    </label>
                    <div v-if="course && 'name' in course">
                        <ControlButton @click="enroll">Записаться</ControlButton>
                    </div>
                    <div v-else-if="course" class="text-gray-600">
                        <div>Дата поступления: {{ new Date(course.admission_date).toLocaleDateString() }}</div>
                        <div class="mb-4">Прогресс обучения: {{ course.progress }}%</div>
                        <CommonLink
                            :to="{ name: `intern-my_courses-id`, params: { id: route.params.id } }"
                            text="Перейти в мой курс"
                        />
                    </div>
                </template>
            </InternNameDescriptionCard>
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    import { FetchError } from 'ofetch';
    import { components } from '~/openapi';

    type OneCourse = components['schemas']['OneCourse'];
    type OneUserCourse = components['schemas']['OneUserCourse'];

    const { $api, $toast, $modal } = useNuxtApp();
    const route = useRoute();
    const userStore = useUserStore();
    const pageStore = usePageStore();
    const alreadyEnrolled = ref(true);
    const course = ref<OneCourse | OneUserCourse>();

    await useAsyncData(async () => {
        try {
            course.value = await $api({
                path: '/api/user/{user_id}/courses/{course_id}',
                method: 'get',
                params: {
                    user_id: userStore.user!.id,
                    course_id: route.params.id as string,
                },
            });
            alreadyEnrolled.value = true;
        } catch (e) {
            if (e instanceof FetchError && e.statusCode === 404) {
                course.value = await $api({
                    path: '/api/courses/{course_id}',
                    method: 'get',
                    params: {
                        course_id: route.params.id as string,
                    },
                });
            } else {
                throw e;
            }
        }
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

    const courseName = computed(() => {
        if (!course.value) {
            return '';
        }
        if ('course_name' in course.value) {
            return course.value.course_name;
        }
        return course.value.name;
    });

    const courseDescription = computed(() => {
        if (!course.value) {
            return '';
        }
        if ('course_description' in course.value) {
            return course.value.course_description;
        }
        return course.value.description;
    });

    function enroll() {
        $modal.show({
            title: DEFAULT_MODAL_TITLE,
            body: `Вы действительно хотите записаться на курс "${courseName.value}"?`,
            type: 'info',
            primary: {
                label: 'Подтвердить',
                theme: 'blue',
                action: async () => {
                    await $api({
                        path: '/api/user/{user_id}/courses/',
                        method: 'post',
                        params: { user_id: userStore.user!.id },
                        body: {
                            course_id: course.value?.id,
                        },
                    });
                    $toast.show({
                        type: 'success',
                        message: `Вы записались на курс ${courseName.value}`,
                        timeout: 4,
                    });
                    return navigateTo({ name: 'intern-my_courses' });
                },
            },
            secondary: DEFAULT_SECONDARY_MODAL_BUTTON_OPTIONS,
        });
    }
</script>
