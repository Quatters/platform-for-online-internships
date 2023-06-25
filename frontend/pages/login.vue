<template>
    <div class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
        <div class="w-full bg-white rounded-lg shadow md:mt-0 sm:max-w-md xl:p-0">
            <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
                <h1 class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl">Вход в аккаунт</h1>
                <form @submit.prevent="submit">
                    <ControlFormInput
                        id="email"
                        v-model="email"
                        label="Email"
                        required
                        placeholder="name@mail.com"
                        type="email"
                        name="email"
                        class="mb-5"
                    />
                    <ControlFormInput
                        id="password"
                        v-model="password"
                        label="Пароль"
                        required
                        placeholder="••••••••"
                        type="password"
                        name="password"
                    />
                    <button
                        type="submit"
                        class="w-full text-white bg-blue-800 hover:bg-blue-700 align-middle transition-colors duration-50 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded px-5 h-10 text-center mt-8 flex justify-center items-center"
                        :disabled="$isFetching"
                    >
                        <UtilSpinner v-if="$isFetching" :size="5" />
                        <div v-else>Войти</div>
                    </button>
                    <div v-show="loginError" class="text-center mt-3 text-red-600 text-sm">
                        Не удалось войти. Проверьте введённые данные.
                    </div>
                </form>
                <div>
                    <p>Нет аккаунта?</p>
                    <NuxtLink :to="{ name: 'intern_register' }" class="link">Регистрация для стажера</NuxtLink>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    const { $isFetching } = useNuxtApp();
    const userStore = useUserStore();

    const email = ref('');
    const password = ref('');
    const loginError = ref(false);

    definePageMeta({
        layout: 'clean',
    });

    async function submit() {
        try {
            await userStore.fetchToken({ email: email.value, password: password.value });
            await userStore.fetchUser({ force: true });
            loginError.value = false;
            return navigateTo({ name: 'index' });
        } catch (e) {
            console.error(e);
            loginError.value = true;
        }
    }
</script>
