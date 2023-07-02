import { FetchError } from 'ofetch';
import { defineStore } from 'pinia';
import { useStorage } from '@vueuse/core';
import { components } from 'openapi';

export default defineStore('user', () => {
    const { $api } = useNuxtApp();
    const accessToken = useStorage('accessToken', '');
    const user = ref<components['schemas']['User']>();

    async function fetchToken({ email, password }: { email: string; password: string }) {
        const response = await $api({
            path: '/api/auth/token',
            method: 'post',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: {
                username: email,
                password,
            },
        });
        accessToken.value = response.access_token;
    }

    async function _fetchUser() {
        try {
            user.value = await $api({
                path: '/api/users/me',
                method: 'get',
            });
        } catch (e) {
            if (e instanceof FetchError && e.status === 401) {
                return;
            }
            throw e;
        }
    }

    async function fetchUser({ force = false } = {}) {
        if (!user.value || force) {
            await _fetchUser();
        }
    }

    function logout() {
        user.value = undefined;
        accessToken.value = '';
    }

    return {
        user,
        fetchUser,
        fetchToken,
        logout,
        accessToken,
    };
});
