export default defineNuxtRouteMiddleware(async () => {
    const userStore = useUserStore();
    await userStore.fetchUser();

    if (userStore.user && !userStore.user.is_admin && !userStore.user.is_teacher) {
        const goingTestStore = useGoingTestStore();
        goingTestStore.fetch();
    }
});
