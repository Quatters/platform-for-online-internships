import { FetchError } from 'ofetch';
import { defineStore } from 'pinia';
import { components } from 'openapi';
import { useStorage } from '@vueuse/core';

export default defineStore('user', () => {
    const { $api } = useNuxtApp();
    const accessToken = useStorage('accessToken', '');
    const user = ref<components['schemas']['User']>();

    async function fetchToken({ email, password }: { email: string; password: string }) {
        const { access_token } = await $api({
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
        accessToken.value = access_token;
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
            console.error(e);
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
    };
});
