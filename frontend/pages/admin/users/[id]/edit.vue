<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
            </template>
        </ControlPanel>
        <CommonContent>
            <ControlForm @submit="save">
                <ControlFormInput v-model="patchData.email" label="Email" class="mb-3" />
                <ControlFormInput v-model="patchData.first_name" label="Имя" class="mb-3" />
                <ControlFormInput v-model="patchData.last_name" label="Фамилия" class="mb-3" />
                <ControlFormInput v-model="patchData.patronymic" label="Отчество" class="mb-3" />
                <ControlFormM2MField v-model="patchData.posts" path="/api/posts" label="Должности" class="mb-3" />
            </ControlForm>
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    import { components } from '~/openapi';

    const { $api } = useNuxtApp();
    const route = useRoute();
    const { navigateBackwards } = useRouteUtils();

    type schema = components['schemas']['PatchUser'];

    const { data } = await useAsyncData(() => {
        return $api({
            path: '/api/users/{user_id}',
            method: 'get',
            params: {
                user_id: route.params.id as string,
            },
        });
    });

    const { patchData } = usePatchDataInitializer<schema>(data, { m2mFields: ['posts'] });

    async function save() {
        await $api({
            path: '/api/users/{user_id}',
            method: 'patch',
            params: {
                user_id: route.params.id as string,
            },
            body: patchData.value,
        });
        return navigateBackwards();
    }
</script>
