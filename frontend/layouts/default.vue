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
            { link: '/intern/my_tasks', title: 'Мои задания' },
            { separator: true },
            { link: '/intern/my_courses', title: 'Мои курсы' },
            { link: '/intern/courses', title: 'Курсы' },
            { separator: true },
            { action: logoutAction, title: 'Выход' },
        ],
        teacher: [
            { link: '/teacher', title: 'Стажёры' },
            { link: '/teacher/tasks', title: 'Задания' },
            { separator: true },
            { action: logoutAction, title: 'Выход' },
        ],
        admin: [
            { link: '/admin/subdivisions', title: 'Подразделения' },
            { link: '/admin/courses', title: 'Курсы' },
            { separator: true },
            { action: logoutAction, title: 'Выход' },
        ],
    };

    const role: Role = userStore.user?.is_admin ? 'admin' : userStore.user?.is_teacher ? 'teacher' : 'intern';
</script>
