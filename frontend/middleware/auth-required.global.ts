export default defineNuxtRouteMiddleware(async to => {
    if (to.name === 'login') {
        return;
    }

    const userStore = useUserStore();
    await userStore.fetchUser();
    if (!userStore.user) {
        return navigateTo({ name: 'login' });
    }
});
