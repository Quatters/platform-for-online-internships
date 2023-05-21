<template>
    <div class="relative w-fit ml-auto">
        <button
            class="absolute top-0 bottom-0 right-0 text-gray-500 font-bold focus:text-blue-800 hover:text-blue-600 transition-colors duration-100 px-3"
            @click="() => setSearch(undefined)"
        >
            ⨯
        </button>
        <ControlInput
            class="ml-auto w-full"
            :class="inputClass"
            placeholder="Найти..."
            :debounce="350"
            :model-value="modelValue"
            @update:model-value="value => setSearch(value)"
        />
    </div>
</template>

<script setup lang="ts">
    const route = useRoute();
    const router = useRouter();

    const props = withDefaults(
        defineProps<{
            modelValue?: string | null;
            emitOnly?: boolean;
            inputClass?: string;
        }>(),
        {
            inputClass: '',
            modelValue: undefined,
        },
    );

    const emit = defineEmits<{
        (e: 'update:modelValue', value?: string): void;
    }>();

    function setSearch(value?: string) {
        value = value || undefined;
        if (!props.emitOnly) {
            router.replace({
                ...route,
                query: {
                    ...route.query,
                    search: value,
                },
            });
        }
        emit('update:modelValue', value);
    }
</script>
