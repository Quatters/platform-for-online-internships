export default function () {
    const router = useRouter();

    function navigateBackwards() {
        let path = router.currentRoute.value.path;
        if (path.endsWith('/')) {
            path = path.slice(0, -1);
        }
        return router.push(router.currentRoute.value.path.split('/').slice(0, -1).join('/'));
    }

    return {
        navigateBackwards,
    };
}
