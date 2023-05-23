import { Breadcrumb } from '~/types';

export default defineNuxtRouteMiddleware(to => {
    const pageStore = usePageStore();

    const breadcrumbs: Breadcrumb[] = [];
    const parts = to.path.split('/');
    const names = [parts[1]];
    for (const part of parts.slice(2)) {
        names.push(part);
        breadcrumbs.push({
            name: capitalize(part),
            to: {
                path: '/' + names.join('/'),
            },
        });
    }

    pageStore.breadcrumbs = breadcrumbs;
});
