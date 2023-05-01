<template>
    <div class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
        <div class="w-full bg-white rounded-lg shadow md:mt-0 sm:max-w-md xl:p-0">
            <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
                <h1 class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl">Вход в аккаунт</h1>
                <form @submit.prevent="submit">
                    <div>
                        <label for="email" class="block mb-2 text-sm font-medium text-gray-900">Эл. почта</label>
                        <input
                            type="email"
                            name="email"
                            id="email"
                            class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5"
                            placeholder="name@mail.com"
                            required
                            v-model="email"
                        />
                    </div>
                    <div class="mt-3">
                        <label for="password" class="block mb-2 text-sm font-medium text-gray-900">Пароль</label>
                        <input
                            type="password"
                            name="password"
                            id="password"
                            placeholder="••••••••"
                            class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5"
                            required
                            v-model="password"
                        />
                    </div>
                    <button
                        type="submit"
                        class="w-full text-white bg-indigo-600 hover:bg-indigo-700 transition-colors duration-50 focus:ring-4 focus:outline-none focus:ring-indigo-300 font-medium rounded-lg px-5 h-11 text-center mt-9"
                        :disabled="$isFetching"
                    >
                        <div>Войти</div>
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
    import { components } from '~/openapi';

    const { $isFetching } = useNuxtApp();
    const userStore = useUserStore();

    const email = ref('');
    const password = ref('');
    const loginError = ref(false);

    definePageMeta({
        layout: 'clean',
    });

    function redirect(user: components['schemas']['User']) {
        let path = '/intern/dashboard';
        if (user.is_admin) {
            path = '/';
        } else if (user.is_teacher) {
            path = '/teacher/interns';
        }
        return navigateTo({ path });
    }

    async function submit() {
        try {
            loginError.value = false;
            await userStore.fetchToken({ email: email.value, password: password.value });
            await userStore.fetchUser({ force: true });
            return redirect(userStore.user!);
        } catch (e) {
            console.log(e);
            loginError.value = true;
        }
    }
</script>
