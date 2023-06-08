<template>
    <div ref="wrapper">
        <button
            type="button"
            class="absolute inline-flex items-center p-1 mt-[1.41rem] ml-3 text-sm rounded-lg md:hidden focus:ring-2 focus:ring-blue-500 hover:text-blue-500 focus:text-blue-500 text-blue-800 transition-all duration-100"
            @click="showSidebar"
        >
            <span class="sr-only">Открыть боковую панель</span>
            <svg
                class="w-6 h-6"
                aria-hidden="true"
                fill="currentColor"
                viewBox="0 0 20 20"
                xmlns="http://www.w3.org/2000/svg"
            >
                <path
                    clip-rule="evenodd"
                    fill-rule="evenodd"
                    d="M2 4.75A.75.75 0 012.75 4h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 4.75zm0 10.5a.75.75 0 01.75-.75h7.5a.75.75 0 010 1.5h-7.5a.75.75 0 01-.75-.75zM2 10a.75.75 0 01.75-.75h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 10z"
                ></path>
            </svg>
        </button>
        <aside
            ref="sidebar"
            class="fixed md:sticky top-0 left-0 z-40 min-w-[19rem] h-screen transition-transform -translate-x-full md:translate-x-0 bg-white shadow-md"
            @click="hideModal"
        >
            <div class="min-w-[inherit]">
                <div class="flex items-center justify-center py-6">
                    <h1 class="text-xl uppercase text-blue-800 font-medium">
                        Платформа
                        <br />
                        онлайн-стажировок
                    </h1>
                </div>
                <ul class="flex flex-col">
                    <li v-for="(item, idx) in sidebarItems" :key="idx">
                        <div v-if="item.separator" class="my-6" />
                        <button
                            v-else-if="item.action"
                            class="flex flex-row items-center text-blue-900 mx-3 mt-2 py-1 ps-7 sidebar-link"
                            @click="item.action"
                        >
                            <div class="w-5 h-5 rounded-full bg-blue-200 circle transition-all duration-100" />
                            <div class="mx-5 title transition-all duration-100">{{ item.title }}</div>
                        </button>
                        <CommonSidebarLink v-else-if="item.link" :to="item.link" :title="item.title" />
                    </li>
                    <li v-if="testStore.test && route.name !== 'intern-tests-current'" class="my-6">
                        <CommonSidebarLink :to="{ name: 'intern-tests-current' }" title="Вернуться к тесту" />
                    </li>
                </ul>
            </div>
        </aside>
    </div>
</template>

<script setup lang="ts">
    import { onClickOutside } from '@vueuse/core';
    import type { SidebarItem } from '~/types';

    defineProps<{
        sidebarItems: SidebarItem[];
    }>();

    const testStore = useTestStore();
    const route = useRoute();

    const sidebar = ref<HTMLElement>();
    const wrapper = ref<HTMLElement>();

    function showSidebar() {
        sidebar.value!.classList.remove('-translate-x-full');
    }

    function hideModal() {
        sidebar.value!.classList.add('-translate-x-full');
    }

    onClickOutside(wrapper, hideModal);
</script>
