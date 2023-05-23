import { FetchError } from 'ofetch';
import type { ToastProps } from 'node_modules/tailvue';

function getMessage(data: any) {
    let message = String(data);
    if (typeof data === 'object' && !Array.isArray(data)) {
        if (data.code === 'integrity_error') {
            message = 'Объект нарушает целостность';
            if (data.original_message) {
                message += `. Подробнее: ${data.original_message}`;
            }
        } else {
            message = JSON.stringify(data);
        }
    }
    return message;
}

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
            toastOptions.message = getMessage(error.data);
        }
        $toast.show(toastOptions);
        console.error(error);
    };
});
