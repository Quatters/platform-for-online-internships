export default defineNuxtRouteMiddleware(async to => {
    const userStore = useUserStore();
    await userStore.fetchUser();

    if (!userStore.user || userStore.user.is_admin) {
        return;
    }

    const { $api } = useNuxtApp();

    if (userStore.user.is_teacher) {
        //
    } else {
        //
    }
});
