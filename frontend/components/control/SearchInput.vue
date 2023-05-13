<template>
    <div class="relative justify-end">
        <button
            class="absolute top-0 bottom-0 right-0 text-gray-500 font-bold focus:text-blue-800 hover:text-blue-600 transition-colors duration-100 px-3"
            @click="() => setSearch(undefined)"
        >
            ⨯
        </button>
        <ControlInput
            class="ml-auto"
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

    defineProps<{
        modelValue?: string | null;
    }>();

    const emit = defineEmits<{
        (e: 'update:modelValue', value?: string): void;
    }>();

    function setSearch(value?: string) {
        value = value || undefined;
        router.replace({
            ...route,
            query: {
                ...route.query,
                search: value,
            },
        });
        emit('update:modelValue', value);
    }
</script>
