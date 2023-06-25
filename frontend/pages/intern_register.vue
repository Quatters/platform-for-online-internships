<template>
    <div class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
        <div class="w-full bg-white rounded-lg shadow md:mt-0 sm:max-w-md xl:p-0">
            <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
                <h1 class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl">Регистрация</h1>
                <form @submit.prevent="register()">
                    <ControlFormInput v-model="data.last_name" label="Фамилия" class="mb-5" />
                    <ControlFormInput v-model="data.first_name" label="Имя" class="mb-5" />
                    <ControlFormInput v-model="data.patronymic" label="Отчество" class="mb-5" />
                    <ControlFormInput
                        v-model="data.email"
                        label="Email"
                        required
                        type="email"
                        class="mb-5"
                        placeholder="name@mail.com"
                    />
                    <ControlFormInput
                        v-model="data.password"
                        label="Пароль"
                        required
                        type="password"
                        class="mb-5"
                        placeholder="••••••••"
                    />

                    <details>
                        <summary class="cursor-pointer">Должности, на которые я хочу обучаться</summary>
                        <div class="mt-2">
                            <div class="mx-[1rem]">
                                <p>Выберите подразделение</p>
                                <ControlSearchInput v-model="searchSubdivisions" emit-only class="my-2 w-full" />
                                <div class="max-h-[8rem] overflow-auto">
                                    <label
                                        v-for="subdivision in subdivisions.items"
                                        :key="subdivision.id"
                                        class="cursor-pointer block"
                                    >
                                        <input
                                            type="radio"
                                            name="subdivision"
                                            class="cursor-pointer"
                                            @click="(e: Event) => selectSubdivision(subdivision.id, (e.target as HTMLInputElement).checked)"
                                        />
                                        <span class="ms-1">{{ subdivision.name }}</span>
                                    </label>
                                    <CommonLoadMore :response="subdivisions" @load-needed="loadMoreSubdivisions" />
                                </div>
                            </div>
                            <div v-if="posts" class="mx-[1rem] mt-4">
                                <p>Выберите должность</p>
                                <ControlSearchInput v-model="searchPosts" emit-only class="my-2 w-full" />
                                <div class="h-30 overflow-auto">
                                    <label v-for="post in posts.items" :key="post.id" class="cursor-pointer block">
                                        <input
                                            type="checkbox"
                                            name="post"
                                            class="cursor-pointer"
                                            @click="(e: Event) => selectPost(post.id, (e.target as HTMLInputElement).checked)"
                                        />
                                        <span class="ms-1">{{ post.name }}</span>
                                    </label>
                                    <CommonLoadMore :response="posts" @load-needed="loadMorePosts" />
                                </div>
                            </div>
                        </div>
                    </details>

                    <button
                        type="submit"
                        class="w-full text-white bg-blue-800 hover:bg-blue-700 align-middle transition-colors duration-50 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded px-5 h-10 text-center mt-8 flex justify-center items-center"
                        :disabled="$isFetching"
                    >
                        <UtilSpinner v-if="$isFetching" :size="5" />
                        <div v-else>Зарегистрироваться</div>
                    </button>
                    <div v-show="error" class="text-center mt-3 text-red-600 text-sm">{{ error }}</div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { FetchError } from 'ofetch';

    definePageMeta({
        layout: 'clean',
    });

    const { $api, $isFetching, $toast } = useNuxtApp();

    const data = ref({
        first_name: '',
        last_name: '',
        patronymic: '',
        email: '',
        password: '',
        posts: [] as Array<number>,
    });

    const searchSubdivisions = ref<string>();
    const searchPosts = ref<string>();
    const selectedSubdivision = ref(-1);

    const error = ref<string>();

    const { data: subdivisions, loadMore: loadMoreSubdivisions } = await useListLoader({
        path: '/api/subdivisions/',
        method: 'get',
        watchQuery: {
            search: searchSubdivisions,
        },
    });

    const { data: posts, loadMore: loadMorePosts } = await useListLoader({
        path: '/api/posts',
        method: 'get',
        watchQuery: {
            subdivision_id: selectedSubdivision,
            search: searchPosts,
        },
    });

    function selectSubdivision(subdivision: number, checked: boolean) {
        if (!checked) {
            return;
        }
        selectedSubdivision.value = subdivision;
        data.value.posts = [];
    }

    function selectPost(post: number, checked: boolean) {
        if (checked) {
            data.value.posts.push(post);
        } else {
            data.value.posts = data.value.posts.filter(key => key !== post);
        }
    }

    async function register() {
        try {
            await $api({
                path: '/api/auth/register',
                method: 'post',
                body: data.value,
            });
        } catch (e) {
            if (e instanceof FetchError && e.statusCode === 400 && e.data?.code === 'integrity_error') {
                error.value = 'Указанный email уже занят.';
                return;
            } else {
                throw e;
            }
        }
        error.value = undefined;
        $toast.show({
            timeout: 4,
            message: 'Вы успешно зарегистрировались. Пожалуйста, выполните вход.',
            type: 'success',
        });
        return navigateTo({ name: 'login' });
    }
</script>
