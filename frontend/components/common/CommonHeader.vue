<template>
    <div class="flex justify-end items-center h-20 mx-8 border-b-2 border-blue-100">
        <div class="me-auto flex items-center ml-4 md:ml-0 w-full h-full overflow-x-auto">
            <div v-for="(breadcrumb, idx) in pageStore.breadcrumbs" :key="idx">
                <NuxtLink :to="breadcrumb.to" class="link mx-1 inline">
                    {{ $t(breadcrumb.name) }}
                </NuxtLink>
                <span>/</span>
            </div>
        </div>
        <div class="flex items-center">
            <div class="w-14 h-14 me-2 rounded-full bg-blue-200"></div>
            <div>
                <div class="font-medium">
                    {{ displayName }}
                </div>
                <div class="text-sm">
                    {{ displayRole }}
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    const userStore = useUserStore();
    const pageStore = usePageStore();

    const displayName = computed(() => {
        return userStore.user?.first_name || userStore.user?.email;
    });

    const displayRole = computed(() => {
        return userStore.user?.is_admin ? 'Администратор' : userStore.user?.is_teacher ? 'Наставник' : 'Стажёр';
    });
</script>
