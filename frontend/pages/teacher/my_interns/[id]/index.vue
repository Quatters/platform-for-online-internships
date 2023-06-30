<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
                <ControlButtonDelete
                    path="/api/users/{intern_id}"
                    :params="{
                        intern_id: route.params.id as string,
                    }"
                    confirm-body="Вы действительно хотите открепить этого стажера от наставника?"
                    text="Открепить"
                    success-title="Стажер успешно откреплен"
                />
            </template>
            <template #links>
                <NuxtLink
                    :to="{ name: 'teacher-my_interns-id-chat', params: { id: route.params.id } }"
                    class="btn-link"
                >
                    Чат
                </NuxtLink>
            </template>
        </ControlPanel>
        <CommonContent>
            <CommonDetailViewCard :item="data!" :hide-fields="['is_admin', 'is_teacher', 'teacher']" />
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const { $api } = useNuxtApp();

    const route = useRoute();
    const userStore = useUserStore();

    const { data } = await useAsyncData(() => {
        return $api({
            path: '/api/users/{teacher_id}/assigned_interns/{intern_id}',
            method: 'get',
            params: {
                teacher_id: userStore.user!.id,
                intern_id: route.params.id as string,
            },
        });
    });
</script>
