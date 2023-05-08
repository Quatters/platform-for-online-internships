<template>
    <div class="min-h-screen flex flex-row bg-blue-50">
        <CommonSidebar :sidebar-items="sidebarItems[role]" />
        <div class="container">
            <CommonHeader />
            <slot></slot>
        </div>
    </div>
</template>

<script setup lang="ts">
    const userStore = useUserStore();

    const sidebarItems = {
        intern: [
            { link: '/intern/dashboard', title: 'Личный кабинет' },
            { link: '/intern/my_tasks', title: 'Мои задания' },
            { separator: true },
            { link: '/intern/courses', title: 'Курсы' },
            { link: '/intern/internships', title: 'Стажировки' },
            { separator: true },
            { link: '/logout', title: 'Выход' },
        ],
        teacher: [
            { link: '/teacher/interns', title: 'Стажёры' },
            { link: '/teacher/tasks', title: 'Задания' },
            { separator: true },
            { link: '/logout', title: 'Выход' },
        ],
        admin: [{ link: '/admin/courses', title: 'Курсы' }, { separator: true }, { link: '/logout', title: 'Выход' }],
    };

    const role: keyof typeof sidebarItems = userStore.user?.is_admin
        ? 'admin'
        : userStore.user?.is_teacher
        ? 'teacher'
        : 'intern';
</script>
