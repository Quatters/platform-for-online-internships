<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
            </template>
        </ControlPanel>
        <CommonContent>
            <CommonCard>
                <div class="text-lg border-b pb-3 mb-3">
                    {{ courseName }}
                </div>
                <div class="pb-3 mb-3 border-b">
                    <div v-if="!courseDescription" class="text-gray-600">Об этом курсе нет информации.</div>
                    <div v-else class="whitespace-pre">
                        {{ courseDescription }}
                    </div>
                </div>
                <div v-if="course && 'name' in course">
                    <ControlButton @click="enroll">Записаться</ControlButton>
                </div>
                <div v-else-if="course" class="text-gray-600">
                    <div>Дата поступления: {{ new Date(course.admission_date).toLocaleDateString() }}</div>
                    <div class="mb-3">Прогресс обучения: {{ course.progress }}%</div>
                    <CommonLink
                        :to="{ name: `intern-my_courses-id`, params: { id: route.params.id } }"
                        text="Перейти в мой курс"
                    />
                </div>
            </CommonCard>
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
    const alreadyEnrolled = ref(true);
    const course = ref<OneCourse | OneUserCourse>();
    usePageStore().name = 'Курсы';

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
                console.error(e);
            }
        }
    });

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
