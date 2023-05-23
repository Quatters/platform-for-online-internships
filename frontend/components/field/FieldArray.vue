<template>
    <ul v-if="shownItems.length">
        <li v-for="(item, idx) in shownItems" :key="idx">{{ item }}</li>
    </ul>
    <div v-else class="text-gray-600 italic">нет</div>
</template>

<script setup lang="ts">
    import { FieldProps } from '~/types';
    interface Item {
        [key: string]: unknown;
    }

    const props = defineProps<FieldProps>();

    const typedValue = ref<Array<Item>>(props.value as Array<Item>);

    const shownItems = computed(() => {
        return typedValue.value.map(item =>
            Object.values(Object.fromEntries(Object.entries(item).filter(([key]) => key !== 'id'))).join(', '),
        );
    });
</script>
