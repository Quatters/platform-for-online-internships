import { useStorage } from '@vueuse/core';
import { APIMethod, APIPath, APIResponseBody, HttpMethod, APIRequestBody, ContentType } from '~/types';

interface Options<P extends APIPath, M extends APIMethod<P>, CT extends ContentType> {
    path: P;
    method: M;
    body?: APIRequestBody<P, M, CT> | URLSearchParams;
    headers?: {
        'Content-Type': CT;
        [key: string]: string;
    };
    params?: Record<string, string | number>;
}

const baseHeaders = {
    'Content-Type': 'application/json',
};

export default defineNuxtPlugin(() => {
    const config = useRuntimeConfig();
    const accessToken = useStorage('accessToken', '');

    const isFetching = ref(false);

    const _api = $fetch.create({
        baseURL: config.public.apiUrl,
        onRequest() {
            isFetching.value = true;
        },
        onResponse() {
            isFetching.value = false;
        },
    });

    function api<P extends APIPath, M extends APIMethod<P>, CT extends ContentType>(options: Options<P, M, CT>) {
        isFetching.value = true;
        const body =
            options.method === 'post' &&
            options.headers &&
            options.headers['Content-Type'] === 'application/x-www-form-urlencoded'
                ? new URLSearchParams(options.body!)
                : options.body;

        const additionalHeaders: Record<string, string> = {};
        if (accessToken.value) {
            additionalHeaders.Authorization = `Bearer ${accessToken.value}`;
        }

        let renderedPath: string = options.path;
        if (options.params) {
            for (const [key, value] of Object.entries(options.params)) {
                renderedPath = renderedPath.replaceAll(`{${key}}`, String(value));
            }
        }

        return _api<APIResponseBody<P, M>>(renderedPath, {
            method: (options.method as string).toUpperCase() as HttpMethod,
            body: body as Record<string, unknown> | URLSearchParams | undefined,
            headers: {
                ...baseHeaders,
                ...additionalHeaders,
                ...(options.headers ? options.headers : {}),
            },
        });
    }

    return {
        provide: {
            api,
            isFetching,
        },
    };
});
