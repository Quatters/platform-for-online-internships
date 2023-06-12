<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
            </template>
        </ControlPanel>
        <CommonContent>
            <ControlForm @submit="save">
                <ControlFormM2MField
                    v-model="data.interns"
                    label="Стажеры"
                    path="/api/users/{teacher_id}/suitable_for_assign_interns"
                    view-field-name="email"
                    :params="{ teacher_id: userStore.user!.id }"
                    class="mb-4"
                />
            </ControlForm>
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    import { components } from '~/openapi';

    const { $api } = useNuxtApp();
    const { navigateBackwards } = useRouteUtils();

    type schema = components['schemas']['AssignInterns'];

    const route = useRoute();
    const userStore = useUserStore();

    const data = ref<schema>({
        interns: [],
    });

    async function save() {
        await $api({
            path: '/api/users/{teacher_id}/assigned_interns',
            params: { teacher_id: userStore.user!.id },
            method: 'put',
            body: data.value,
        });
        return navigateBackwards();
    }
</script>
