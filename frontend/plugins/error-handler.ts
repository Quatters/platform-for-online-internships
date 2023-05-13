export default defineNuxtPlugin(nuxtApp => {
    const { $toast } = useNuxtApp();
    nuxtApp.vueApp.config.errorHandler = (error, _) => {
        if (error) {
            $toast.show({
                type: 'danger',
                title: 'Неизвестная ошибка',
                timeout: 4,
                message: 'Если что-то пошло не так, попробуйте перезагрузить страницу.',
            });
            console.error(error);
        }
    };
});
