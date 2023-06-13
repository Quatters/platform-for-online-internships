<template>
    <div></div>
</template>

<script setup lang="ts">
    const userStore = useUserStore();

    if (userStore.user?.is_admin) {
        navigateTo({ name: 'admin-courses' });
    } else if (userStore.user?.is_teacher) {
        navigateTo({ name: 'teacher-my_interns' });
    } else {
        navigateTo({ name: 'intern-dashboard' });
    }
</script>
