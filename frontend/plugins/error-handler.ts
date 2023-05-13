import { FetchError } from 'ofetch';
import type { ToastProps } from 'node_modules/tailvue';

export default defineNuxtPlugin(nuxtApp => {
    const { $toast } = useNuxtApp();
    nuxtApp.vueApp.config.errorHandler = (error, _) => {
        if (!error) {
            return;
        }
        const toastOptions: ToastProps = {
            type: 'danger',
            title: 'Неизвестная ошибка',
            timeout: 4,
        };
        if (error instanceof FetchError) {
            toastOptions.title = 'Ошибка соединения с сервером';
            toastOptions.message = 'Не удалось выполнить запрос или запрос выполнен неуспешно.';
        }
        $toast.show(toastOptions);
        console.error(error);
    };
});
