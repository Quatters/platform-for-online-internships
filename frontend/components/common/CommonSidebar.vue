<template>
    <div class="min-h-screen flex flex-row bg-gray-100">
        <div class="flex flex-col w-72 bg-white overflow-hidden">
            <div class="flex items-center justify-center py-4 border-b-2">
                <h1 class="text-xl uppercase text-indigo-600 font-medium">
                    Платформа
                    <br />
                    онлайн-стажировок
                </h1>
            </div>
            <ul class="flex flex-col">
                <li v-for="item in sidebarItems">
                    <NuxtLink
                        :to="item.link"
                        class="flex flex-row items-center transition-colors duration-50 font-medium text-gray-600 hover:bg-indigo-50 rounded-e-full me-2 mt-2 py-3"
                    >
                        <div
                            v-if="router.currentRoute.value.fullPath === item.link"
                            class="bg-indigo-500 h-full w-3 rounded-e-full"
                        >
                            &nbsp;
                        </div>
                        <div class="mx-6">{{ item.title }}</div>
                    </NuxtLink>
                </li>
            </ul>
        </div>
    </div>
</template>

<script setup lang="ts">
    interface SidebarItem {
        title: string;
        link: string;
    }

    defineProps<{
        sidebarItems: SidebarItem[];
    }>();

    const router = useRouter();
</script>
