<template>
    <div>
        <ControlFormLabel :value="label" :required="required" />
        <div ref="wrapper" class="relative">
            <button
                type="button"
                class="flex shadow appearance-none border border-gray-300 rounded w-full h-[2.385rem] overflow-x-hidden text-ellipsis py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
                :class="{ 'border-b-0 rounded-b-none': dropdownShown }"
                @click="showDropdown"
            >
                <span v-if="modelValue">{{ viewValue ?? $t(modelValue) }}</span>
                <span v-else class="italic text-gray-500">нет</span>
                <button
                    v-if="!required"
                    class="absolute top-0 bottom-0 right-0 text-gray-500 font-bold focus:text-blue-800 hover:text-blue-600 transition-colors duration-100 px-3"
                    type="button"
                    @click="() => setValue({ modelValue: undefined, viewValue: undefined })"
                >
                    ⨯
                </button>
            </button>
            <div v-if="dropdownShown">
                <ul
                    class="absolute w-full shadow border rounded rounded-t-none bg-white max-h-96 overflow-y-auto z-50"
                    @click="hideDropdown"
                >
                    <li
                        v-for="item in items"
                        :key="item.value"
                        class="hover:bg-gray-100 cursor-pointer py-1 px-3 border-t"
                        @click="() => setValue({ modelValue: item.value, viewValue: item.viewValue })"
                    >
                        {{ item.viewValue ?? $t(item.value) }}
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    interface EnumItem {
        value: string;
        viewValue?: string;
    }

    const props = withDefaults(
        defineProps<{
            modelValue?: string | undefined | null;
            viewValue?: string | number;
            required?: boolean;
            label: string;
            enumItems: EnumItem[] | string[];
        }>(),
        {
            modelValue: undefined,
            viewValue: undefined,
            required: false,
        },
    );

    const items = computed(() => {
        if (props.enumItems.length === 0) {
            return [] as EnumItem[];
        }
        if (typeof props.enumItems[0] === 'string') {
            return props.enumItems.map(item => ({ value: item } as EnumItem));
        }
        return props.enumItems as EnumItem[];
    });

    const dropdownShown = ref(false);
    const wrapper = ref<HTMLDivElement>();

    const emit = defineEmits<{
        (e: 'update:modelValue', value: typeof props.modelValue): void;
        (e: 'update:viewValue', value: typeof props.viewValue): void;
    }>();

    function showDropdown() {
        dropdownShown.value = true;
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
