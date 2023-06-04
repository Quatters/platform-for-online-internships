<template>
    <div class="bg-white rounded-md shadow px-6 py-4 grid gap-10">
        <TopicResourceItem v-for="(item, idx) in items" :key="idx" :item="item">
            <NuxtLink v-if="detailLinks" :to="getDetailLink(item)" class="link">Подробнее</NuxtLink>
        </TopicResourceItem>
    </div>
</template>

<script setup lang="ts">
    import type { TopicResourceListItem } from '~/types';

    const props = withDefaults(
        defineProps<{
            items: TopicResourceListItem[];
            detailLinks?: boolean;
            linkParamName?: string;
            apiValueFieldName?: string;
        }>(),
        {
            detailLinks: false,
            linkParamName: 'id',
            apiValueFieldName: 'id',
        },
    );

    const route = useRoute();

    function getDetailLink(item: TopicResourceListItem) {
        return {
            name: `${String(route.name)}-${props.linkParamName}`,
            params: { [props.linkParamName]: String(item[props.apiValueFieldName]) },
        };
    }
</script>
