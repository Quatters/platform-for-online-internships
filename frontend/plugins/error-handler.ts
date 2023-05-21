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
        $toast.show(toastOptions);
        console.error(error);
    };
});
