<template>
    <table class="table-auto border-collapse rounded-md w-full bg-white shadow">
        <thead>
            <tr class="border-b">
                <th v-for="(key, idx) in headerKeys" :key="idx" class="text-left px-4 py-2">{{ $t(key) }}</th>
            </tr>
        </thead>
        <tbody>
            <NuxtLink
                v-for="(item, idx) in items"
                :key="idx"
                v-slot="{ navigate, href }"
                :to="getDetailLink(item)"
                :custom="true"
            >
                <tr class="border-b hover:bg-gray-100 hover:cursor-pointer" :data-href="href" @click.stop="navigate">
                    <td v-for="(value, valueIdx) in getItemValues(item)" :key="valueIdx" class="px-4 py-2">
                        {{ value }}
                    </td>
                </tr>
            </NuxtLink>
        </tbody>
    </table>
</template>

<script setup lang="ts">
    interface Item {
        id: number;
        [key: string]: unknown;
    }

    const props = withDefaults(
        defineProps<{
            items: Item[];
            withId?: boolean;
            linkParamName?: string;
            additionalParams?: Record<string, string>;
        }>(),
        {
            linkParamName: 'id',
            additionalParams: () => ({}),
            withId: false,
        },
    );

    const route = useRoute();

    function getDetailLink(item: Item) {
        return {
            name: `${String(route.name)}-${props.linkParamName}`,
            params: { [props.linkParamName]: String(item.id) },
        };
    }

    function getItemValues(item: Record<string, unknown>) {
        if (props.withId) {
            return Object.values(item);
        }
        return Object.entries(item)
            .filter(obj => obj[0] !== 'id')
            .map(obj => obj[1]);
    }

    const headerKeys = computed(() => {
        if (props.items.length === 0) {
            return [];
        }
        let keys = Object.keys(props.items[0]);
        if (!props.withId) {
            keys = keys.filter(key => key !== 'id');
        }
        return keys.map(value => capitalize(value));
    });
</script>
