export default defineNuxtRouteMiddleware(async to => {
    if (to.name === 'login') {
        return;
    }

    const userStore = useUserStore();
    await userStore.fetchUser();
    if (!userStore.user) {
        return navigateTo({ name: 'login' });
    }

    if (to.path.startsWith('/admin') && !userStore.user.is_admin) {
        throw error404();
    }
    if (to.path.startsWith('/teacher') && !userStore.user.is_teacher) {
        throw error404();
    }
    if ((to.path.startsWith('/intern') && userStore.user.is_admin) || userStore.user.is_teacher) {
        throw error404();
    }
});
