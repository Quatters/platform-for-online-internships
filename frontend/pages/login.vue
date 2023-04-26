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
                        class="w-full text-white bg-indigo-600 hover:bg-indigo-700 transition-colors duration-50 focus:ring-4 focus:outline-none focus:ring-indigo-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mt-9"
                    >
                        Войти
                    </button>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    const email = ref('');
    const password = ref('');

    async function submit() {
        const response = await $fetch('/login', { method: 'post' });
        console.log(response);
    }
</script>
