<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
            </template>
        </ControlPanel>
        <CommonContent>
            <ControlForm @submit="save">
                <ControlFormInput v-model="data.email" type="email" class="mb-4" label="Email" required />
                <ControlFormInput v-model="data.password" type="password" class="mb-4" label="Пароль" required />
                <ControlFormInput v-model="data.first_name" class="mb-4" label="Имя" />
                <ControlFormInput v-model="data.last_name" class="mb-4" label="Фамилия" />
                <ControlFormInput v-model="data.patronymic" class="mb-4" label="Отчество" />
                <ControlFormBooleanField v-model="data.is_admin" class="mb-4" label="Администратор" />
                <ControlFormBooleanField v-model="data.is_teacher" class="mb-4" label="Наставник" />
                <ControlFormM2MField
                    v-show="!data.is_admin"
                    v-model="data.posts"
                    label="Должности"
                    path="/api/posts"
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

    type schema = components['schemas']['CreateUser'];

    const data = ref<schema>({
        first_name: '',
        last_name: '',
        patronymic: '',
        password: '',
        email: '',
        is_admin: false,
        is_teacher: false,
        posts: [],
    });

    watch(toRef(data.value, 'is_admin'), value => {
        if (value) {
            data.value.is_teacher = false;
            data.value.posts = [];
        }
    });

    watch(toRef(data.value, 'is_teacher'), value => {
        if (value) {
            data.value.is_admin = false;
        }
    });

    async function save() {
        await $api({
            path: '/api/users',
            method: 'post',
            body: data.value,
        });
        return navigateBackwards();
    }
</script>
