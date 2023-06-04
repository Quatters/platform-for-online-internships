<template>
    <div>
        <ControlFormLabel :value="label" :required="required" />
        <div ref="wrapper" class="relative">
            <button
                v-if="!dropdownShown"
                type="button"
                class="flex shadow appearance-none border border-gray-300 rounded w-full h-[2.385rem] overflow-x-hidden text-ellipsis py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
                @click="showDropdown"
            >
                <span v-if="modelValue !== undefined">{{ viewValue ?? modelValue }}</span>
                <span v-else class="italic text-gray-500">не задано</span>
                <button
                    v-if="!required"
                    class="absolute top-0 bottom-0 right-0 text-gray-500 font-bold focus:text-blue-800 hover:text-blue-600 transition-colors duration-100 px-3"
                    type="button"
                    @click="() => setValue({ modelValue: undefined, viewValue: undefined })"
                >
                    ⨯
                </button>
            </button>
            <div v-else>
                <ControlSearchInput
                    ref="searchInput"
                    v-model="search"
                    emit-only
                    class="w-full m-0"
                    input-class="outline-none border-b-0 rounded-b-none h-[2.385rem] py-2 px-3 m-0 text-sm"
                />
                <ul
                    v-if="typedData.items.length"
                    class="absolute w-full shadow border rounded rounded-t-none bg-white max-h-96 overflow-y-auto z-50"
                    @click="hideDropdown"
                >
                    <li
                        v-for="item in typedData.items"
                        :key="item[valueFieldName]"
                        class="hover:bg-gray-100 cursor-pointer py-1 px-3 border-t"
                        @click="() => setValue({ modelValue: item[valueFieldName], viewValue: item[viewFieldName] })"
                    >
                        {{ item[viewFieldName] }}
                    </li>
                    <CommonLoadMore :response="data" class="!mb-0" @load-needed="loadMore" />
                </ul>
                <ul
                    v-else
                    class="absolute w-full shadow border rounded rounded-t-none bg-white max-h-96 overflow-y-auto z-50"
                    @click="hideDropdown"
                >
                    <li class="py-1 px-3 border-t text-gray-600">Не найдено</li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { onClickOutside } from '@vueuse/core';
    import type { ControlSearchInput } from '~/.nuxt/components';
    import type { APIPath, ListItems } from '~/types';

    const props = withDefaults(
        defineProps<{
            modelValue?: number | undefined | null;
            viewValue?: string | number;
            required?: boolean;
            path: APIPath;
            params?: Record<string, string | number>;
            valueFieldName: string;
            viewFieldName: string;
            label: string;
            nullable?: boolean;
        }>(),
        {
            modelValue: undefined,
            viewValue: undefined,
            params: () => ({}),
            required: false,
            valueFieldName: 'id',
            viewFieldName: 'name',
            nullable: false,
        },
    );

    const emit = defineEmits<{
        (e: 'update:modelValue', value: typeof props.modelValue): void;
        (e: 'update:viewValue', value: typeof props.viewValue): void;
    }>();

    const dropdownShown = ref(false);
    const wrapper = ref<HTMLDivElement>();

    const searchInput = ref<InstanceType<typeof ControlSearchInput>>();
    const search = ref<string | undefined>();

    const { data, loadMore } = await useListLoader({
        path: props.path,
        // @ts-expect-error must be list path
        method: 'get',
        params: props.params,
        watchQuery: {
            search,
        },
    });

    const typedData = computed(() => {
        const _typedData = data.value as ListItems;
        if (props.nullable) {
            // @ts-expect-error i'm too lazy to solve this
            _typedData.items.unshift({
                id: 0,
                [props.valueFieldName]: null,
                [props.viewFieldName]: 'пусто',
            });
        }
        return _typedData;
    });

    async function showDropdown() {
        dropdownShown.value = true;
        await nextTick();
        searchInput.value?.controlInput?.$el.focus();
    }

    function hideDropdown() {
        dropdownShown.value = false;
    }

    function setValue({
        modelValue,
        viewValue,
    }: {
        modelValue: typeof props.modelValue;
        viewValue: typeof props.viewValue;
    }) {
        emit('update:modelValue', modelValue);
        emit('update:viewValue', viewValue);
    }

    onMounted(() => {
        onClickOutside(wrapper, hideDropdown);
    });
</script>
