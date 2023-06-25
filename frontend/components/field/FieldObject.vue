<template>
    <div v-if="shownItem.value === null" class="text-gray-600 italic">не задано</div>
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

    const typedValue = computed<Item>(() => props.value as Item);

    function getFkLink(item: Item): RouteLocationNamedRaw {
        const baseLink = pageStore.fkInstancePathMap[props.fieldName];
        const param = baseLink.name!.toString().split('-').slice(-1)[0];

        const fromResponseParams: typeof baseLink.params = {};
        if (pageStore.fkInstancePathMap[props.fieldName].params) {
            // @ts-expect-error i'm too lazy to solve this
            for (const [key, value] of Object.entries(pageStore.fkInstancePathMap[props.fieldName].params)) {
                if (value === '<<from-response>>') {
                    const apiKey = (pageStore.fkInstancePathMap[props.fieldName]?.routerToResponseParamsMap?.[key] ??
                        key) as string;
                    fromResponseParams[key] = item[apiKey] as string;
                }
            }
        }

        return {
            ...baseLink,
            params: {
                ...baseLink.params,
                ...fromResponseParams,
                [param]: item.id as number,
            },
        };
    }

    function getValue(item: Item) {
        const viewFieldName = pageStore.fkInstancePathMap?.[props.fieldName]?.viewFieldName ?? 'name';
        return item[viewFieldName] as string;
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
