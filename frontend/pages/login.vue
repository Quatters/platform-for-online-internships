<template>
    <div class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
        <div class="w-full bg-white rounded-lg shadow md:mt-0 sm:max-w-md xl:p-0">
            <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
                <h1 class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl">Вход в аккаунт</h1>
                <form @submit.prevent="submit">
                    <div>
                        <label for="email" class="block mb-2 text-sm font-medium text-gray-900">Эл. почта</label>
                        <input
                            id="email"
                            v-model="email"
                            type="email"
                            name="email"
                            class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-800 focus:border-blue-800 block w-full p-2.5"
                            placeholder="name@mail.com"
                            required
                        />
                    </div>
                    <div class="mt-3">
                        <label for="password" class="block mb-2 text-sm font-medium text-gray-900">Пароль</label>
                        <input
                            id="password"
                            v-model="password"
                            type="password"
                            name="password"
                            placeholder="••••••••"
                            class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-800 focus:border-blue-800 block w-full p-2.5"
                            required
                        />
                    </div>
                    <button
                        type="submit"
                        class="w-full text-white bg-blue-800 hover:bg-blue-700 align-middle transition-colors duration-50 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg px-5 h-11 text-center mt-9 flex justify-center items-center"
                        :disabled="$isFetching"
                    >
                        <UtilSpinner v-if="$isFetching" :size="5" />
                        <div v-else>Войти</div>
                    </button>
                    <div v-show="loginError" class="text-center mt-3 text-red-600 text-sm">
                        Не удалось войти. Проверьте введённые данные.
                    </div>
                </form>
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
            loginError.value = false;
            await userStore.fetchToken({ email: email.value, password: password.value });
            await userStore.fetchUser({ force: true });
            return navigateTo({ name: 'index' });
        } catch (e) {
            console.error(e);
            loginError.value = true;
        }
    }
</script>
