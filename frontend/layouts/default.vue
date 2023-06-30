<template>
    <div class="min-h-screen flex flex-row bg-blue-50">
        <CommonSidebar :sidebar-items="sidebarItems[role]" />
        <div class="w-full">
            <CommonHeader />
            <slot></slot>
        </div>
    </div>
</template>

<script setup lang="ts">
    import useChatStore from '~/composables/useChatStore';
    import type { SidebarItem } from '~/types';

    const { $modal } = useNuxtApp();
    const userStore = useUserStore();

    const logoutAction = () => {
        $modal.show({
            type: 'danger',
            title: 'Подтвердите действие',
            body: 'Вы действительно хотите выйти из аккаунта?',
            primary: {
                action: () => navigateTo('/logout'),
                theme: 'red',
                label: 'Выйти',
            },
            secondary: DEFAULT_SECONDARY_MODAL_BUTTON_OPTIONS,
        });
    };

    type Role = 'intern' | 'teacher' | 'admin';

    const sidebarItems: Record<Role, SidebarItem[]> = {
        intern: [
            { link: '/intern/dashboard', title: 'Личный кабинет' },
            { separator: true },
            { link: '/intern/my_courses', title: 'Мои курсы' },
            { link: '/intern/tests', title: 'Мои тесты' },
            { separator: true },
            { link: '/intern/courses', title: 'Курсы' },
            { link: '/intern/subdivisions', title: 'Подразделения' },
            { separator: true },
            { action: logoutAction, title: 'Выход' },
        ],
        teacher: [
            { link: '/teacher/my_interns', title: 'Мои стажеры' },
            { link: '/teacher/task_checking', title: 'Проверка заданий' },
            { separator: true },
            { action: logoutAction, title: 'Выход' },
        ],
        admin: [
            { link: '/admin/subdivisions', title: 'Подразделения' },
            { link: '/admin/posts', title: 'Должности' },
            { link: '/admin/courses', title: 'Курсы' },
            { link: '/admin/competencies', title: 'Компетенции' },
            { separator: true },
            { link: '/admin/users', title: 'Пользователи' },
            { separator: true },
            { action: logoutAction, title: 'Выход' },
        ],
    };

    const role: Role = userStore.user?.is_admin ? 'admin' : userStore.user?.is_teacher ? 'teacher' : 'intern';

    if (['intern', 'teacher'].includes(role)) {
        const chatStore = useChatStore();
        chatStore.showNotifications = true;
        chatStore.connect({ force: true });
        if (!userStore.user?.is_admin && !userStore.user?.is_teacher && userStore.user?.teacher) {
            sidebarItems.intern.splice(4, 0, { link: '/intern/chat', title: 'Чат' });
        }
    }
</script>
