<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
                <ControlButtonDelete
                    path="/api/users/{intern_id}"
                    :params="{
                        intern_id: route.params.intern_id as string,
                    }"
                    confirm-body="Вы действительно хотите открепить этого стажера от наставника?"
                    text="Открепить"
                    success-title="Стажер успешно откреплен"
                />
            </template>
            <template #links>
                <NuxtLink
                    v-if="!data?.is_teacher"
                    :to="{ name: 'admin-users-id', params: { id: data.id } }"
                    class="link"
                >
                    Перейти к пользователю
                </NuxtLink>
            </template>
        </ControlPanel>
        <CommonContent>
            <CommonDetailViewCard :item="data!" :hide-fields="['is_admin', 'is_teacher', 'interns']" />
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const { $api } = useNuxtApp();

    const route = useRoute();

    const { data } = await useAsyncData(() => {
        return $api({
            path: '/api/users/{teacher_id}/assigned_interns/{intern_id}',
            method: 'get',
            params: {
                teacher_id: route.params.id as string,
                intern_id: route.params.intern_id as string,
            },
        });
    });
</script>
