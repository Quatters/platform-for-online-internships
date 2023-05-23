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
            title: 'Ошибка',
            message: String(error),
            timeout: 4,
        };
        if (error instanceof FetchError && error.data) {
            toastOptions.message = JSON.stringify(error.data);
        }
        $toast.show(toastOptions);
        console.error(error);
    };
});
