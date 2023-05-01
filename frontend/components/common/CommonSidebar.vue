<template>
    <div class="flex flex-col min-w-[19rem] bg-white overflow-hidden">
        <div class="flex items-center justify-center py-6">
            <h1 class="text-xl uppercase text-blue-800 font-medium">
                Платформа
                <br />
                онлайн-стажировок
            </h1>
        </div>
        <ul class="flex flex-col">
            <li v-for="item in sidebarItems">
                <div v-if="item.separator" class="my-6"></div>
                <NuxtLink v-else :to="item.link" class="flex flex-row items-center text-blue-900 mx-3 mt-2 py-1 ps-7">
                    <div
                        class="w-5 h-5 rounded-full"
                        :class="$route.fullPath === item.link ? 'bg-blue-800' : 'bg-blue-200'"
                    ></div>
                    <div class="mx-5">{{ item.title }}</div>
                </NuxtLink>
            </li>
        </ul>
    </div>
</template>

<script setup lang="ts">
    interface Item {
        title: string;
        link: string;
        separator?: never;
    }

    interface Separator {
        separator: boolean;
        title?: never;
        link?: never;
    }

    defineProps<{
        sidebarItems: (Item | Separator)[];
    }>();
</script>
