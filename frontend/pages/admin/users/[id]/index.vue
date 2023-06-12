<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
                <ControlButtonEdit />
                <ControlButtonDelete path="/api/users/{user_id}" :params="{ user_id: route.params.id as string}" />
                <ControlButtonDelete
                    v-if="data?.teacher"
                    path="/api/users/{intern_id}"
                    :params="{
                        intern_id: route.params.id as string,
                    }"
                    confirm-body="Вы действительно хотите открепить этого стажера от наставника?"
                    text="Открепить"
                    success-title="Стажер успешно откреплен"
                    disable-redirect
                    @success="fetchData()"
                />
            </template>
            <template #links>
                <NuxtLink
                    v-if="data?.is_teacher"
                    :to="{ name: 'admin-users-id-assigned_interns', params: { id: route.params.id } }"
                    class="link"
                >
                    Прикрепленные стажеры
                </NuxtLink>
            </template>
        </ControlPanel>
        <CommonContent>
            <CommonDetailViewCard
                :item="data!"
                :hide-fields="data!.is_admin ? ['posts', 'is_teacher', 'teacher', 'interns'] : data!.is_teacher ? ['is_admin', 'teacher'] : ['is_admin', 'is_teacher', 'interns']"
            />
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    import { components } from '~/openapi';

    const { $api } = useNuxtApp();

    const route = useRoute();

    const pageStore = usePageStore();
    const data = ref<components['schemas']['User']>();

    async function fetchData() {
        data.value = await $api({
            path: '/api/users/{user_id}',
            method: 'get',
            params: {
                user_id: route.params.id as string,
            },
        });
    }

    await useAsyncData(fetchData);

    pageStore.fkInstancePathMap = {
        posts: {
            name: 'admin-subdivisions-id-posts-post_id',
            params: { id: '<<from-response>>', post_id: '<<from-response>>' },
            response: data.value?.posts,
            routerToResponseParamsMap: {
                id: 'subdivision_id',
                post_id: 'post_id',
            },
        },
        teacher: { name: 'admin-users-id', viewFieldName: 'email' },
    };
</script>
