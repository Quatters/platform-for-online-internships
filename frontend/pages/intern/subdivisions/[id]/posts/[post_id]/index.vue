<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
            </template>
        </ControlPanel>
        <CommonContent>
            <InternNameDescriptionCard :name="data!.name" :description="data?.description">
                <template #additional-content>
                    <label class="block py-2 border-t">
                        <span class="inline-block pb-1">Курсы для освоения этой должности</span>
                        <FieldArray :value="data?.courses" field-name="courses" />
                    </label>
                    <label class="block py-2 border-t mb-6">
                        <span class="inline-block pb-1">Компетенции, необходимые для этой должности</span>
                        <FieldArray :value="data?.competencies" field-name="competencies" />
                    </label>
                    <div v-if="canAssign">
                        <ControlButton @click="assign">Начать осваивать</ControlButton>
                    </div>
                    <div v-else>
                        <ControlButton variant="red" @click="unassign">Перестать осваивать</ControlButton>
                    </div>
                </template>
            </InternNameDescriptionCard>
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const { $api, $modal, $toast } = useNuxtApp();

    const route = useRoute();
    const pageStore = usePageStore();
    const userStore = useUserStore();

    pageStore.fkInstancePathMap = {
        courses: {
            name: 'intern-courses-id',
        },
    };

    const { data } = await useAsyncData(() => {
        return $api({
            path: '/api/subdivisions/{subdivision_id}/posts/{post_id}',
            method: 'get',
            params: { subdivision_id: route.params.id as string, post_id: route.params.post_id as string },
        });
    });

    const canAssign = computed(() => {
        const postIds = userStore.user?.posts.map(post => post.id);
        return !postIds?.includes(Number(route.params.post_id));
    });

    function assign() {
        $modal.show({
            title: DEFAULT_MODAL_TITLE,
            body: `Вы действительно хотите начать осваивать должность "${data.value?.name}"?`,
            type: 'info',
            primary: {
                label: 'Подтвердить',
                theme: 'blue',
                action: async () => {
                    await $api({
                        path: '/api/posts/{post_id}/assign',
                        method: 'put',
                        params: {
                            post_id: route.params.post_id as string,
                        },
                    });
                    $toast.show({
                        type: 'success',
                        message: `Вы начали осваивать должность ${data.value?.name}`,
                        timeout: 4,
                    });
                    userStore.fetchUser({ force: true });
                },
            },
            secondary: DEFAULT_SECONDARY_MODAL_BUTTON_OPTIONS,
        });
    }

    function unassign() {
        $modal.show({
            title: DEFAULT_MODAL_TITLE,
            body: `Вы действительно хотите перестать осваивать должность "${data.value?.name}"?`,
            type: 'info',
            primary: {
                label: 'Подтвердить',
                theme: 'red',
                action: async () => {
                    await $api({
                        path: '/api/posts/{post_id}/unassign',
                        method: 'put',
                        params: {
                            post_id: route.params.post_id as string,
                        },
                    });
                    $toast.show({
                        type: 'success',
                        message: `Вы больше не осваиваете должность ${data.value?.name}`,
                        timeout: 4,
                    });
                    userStore.fetchUser({ force: true });
                },
            },
            secondary: DEFAULT_SECONDARY_MODAL_BUTTON_OPTIONS,
        });
    }
</script>
