<template>
    <div>
        <ControlFormLabel :value="label" :required="required" />
        <ControlSearchInput v-model="search" class="w-full mb-3" emit-only />
        <div class="shadow border border-gray-300 rounded p-3 max-h-[8.5rem] overflow-y-auto">
            <div v-if="typedData.items.length">
                <label v-for="item in typedData!.items" :key="item.id" class="block cursor-pointer">
                    <input
                        type="checkbox"
                        name="model"
                        :checked="modelValue.includes(item.id)"
                        class="cursor-pointer ml-1"
                        @click="(e: Event) => change(item.id, (e.target as HTMLInputElement).checked)"
                    />
                    <span class="ml-2">{{ item[viewFieldName] }}</span>
                </label>
            </div>
            <div v-else class="text-gray-600">Не найдено</div>
            <CommonLoadMore :response="data" class="!mb-0" @load-needed="loadMore" />
        </div>
    </div>
</template>

<script setup lang="ts">
    import type { APIPath, ListItems } from '~/types';

    const props = withDefaults(
        defineProps<{
            path: APIPath;
            params?: Record<string, string | number>;
            viewFieldName?: string;
            modelValue?: Array<number>;
            required?: boolean;
            label: string;
        }>(),
        {
            viewFieldName: 'name',
            required: false,
            modelValue: () => [],
            params: () => ({}),
        },
    );

    const emit = defineEmits<{
        (e: 'update:modelValue', value: typeof props.modelValue): void;
    }>();

    const search = ref<string>();

    function change(item: number, checked: boolean) {
        const value = [...props.modelValue];

        if (checked) {
            value.push(item);
            emit('update:modelValue', value);
        } else {
            emit(
                'update:modelValue',
                value.filter(key => key !== item),
            );
        }
    }

    const { data, loadMore } = await useListLoader({
        path: props.path,
        params: props.params,
        // @ts-expect-error must be list path
        method: 'get',
        watchQuery: {
            search,
        },
    });

    const typedData = computed(() => data.value as ListItems);
</script>
