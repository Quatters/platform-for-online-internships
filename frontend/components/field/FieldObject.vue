<template>
    <div v-if="shownItem.value === null" class="text-gray-600 italic">нет</div>
    <NuxtLink v-else-if="shownItem.to" :to="shownItem.to" class="link">
        {{ shownItem.value }}
    </NuxtLink>
    <div v-else>{{ shownItem.value }}</div>
</template>

<script setup lang="ts">
    import { RouteLocationNamedRaw } from 'vue-router';
    import { FieldProps } from '~/types';

    interface Item {
        [key: string]: unknown;
    }

    interface ShownItem {
        to?: RouteLocationNamedRaw;
        value: string | null;
    }

    const pageStore = usePageStore();

    const props = defineProps<FieldProps>();

    const typedValue = ref<Item>(props.value as Item);

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

    const shownItem = computed<ShownItem>(() => {
        if (typedValue.value === null) {
            return { value: null };
        }
        if (typeof typedValue.value.id === 'number' && pageStore.fkInstancePathMap[props.fieldName]) {
            return {
                to: getFkLink(typedValue.value),
                value: getValue(typedValue.value),
            };
        }
        return { value: getValue(typedValue.value) };
    });
</script>
