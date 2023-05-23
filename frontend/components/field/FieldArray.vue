<template>
    <ul v-if="shownItems.length" class="max-h-[8.5rem] overflow-y-auto">
        <li v-for="(item, idx) in shownItems" :key="idx">
            <NuxtLink v-if="item.to" :to="item.to" class="link">
                {{ item.value }}
            </NuxtLink>
            <span v-else>{{ item.value }}</span>
        </li>
    </ul>
    <div v-else class="text-gray-600 italic">нет</div>
</template>

<script setup lang="ts">
    import { RouteLocationNamedRaw } from 'vue-router';
    import { FieldProps } from '~/types';

    interface Item {
        [key: string]: unknown;
    }

    interface ShownItem {
        to?: RouteLocationNamedRaw;
        value: string;
    }

    const pageStore = usePageStore();

    const props = defineProps<FieldProps>();

    const typedValue = ref<Array<Item>>(props.value as Array<Item>);

    function getFkLink(item: Item): RouteLocationNamedRaw {
        const baseLink = pageStore.fkInstancePathMap[props.fieldName];
        const param = baseLink.name!.toString().split('-').slice(-1)[0];
        return {
            ...baseLink,
            params: {
                ...baseLink.params,
                [param]: item.id as number,
            },
        };
    }

    function getValue(item: Item) {
        return Object.values(Object.fromEntries(Object.entries(item).filter(([key]) => key !== 'id'))).join(', ');
    }

    const shownItems = computed<ShownItem[]>(() => {
        if (!typedValue.value.length) {
            return [];
        }
        if (
            typeof typedValue.value[0] === 'object' &&
            typeof typedValue.value[0].id === 'number' &&
            pageStore.fkInstancePathMap[props.fieldName]
        ) {
            return typedValue.value.map(item => ({
                to: getFkLink(item),
                value: getValue(item),
            }));
        }
        return typedValue.value.map(item => getValue(item)).map(value => ({ value }));
    });
</script>
