<template>
    <div class="relative justify-end">
        <button
            class="absolute top-0 bottom-0 right-0 text-gray-500 font-bold focus:text-blue-800 hover:text-blue-600 transition-colors duration-100 px-3"
            @click="clear"
        >
            ⨯
        </button>
        <ControlInput
            class="ml-auto"
            placeholder="Найти..."
            :debounce="350"
            :model-value="modelValue"
            @update:model-value="value => emit('update:modelValue', value)"
        />
    </div>
</template>

<script setup lang="ts">
    defineProps<{
        modelValue?: string;
    }>();

    const emit = defineEmits<{
        (e: 'update:modelValue', value?: string): void;
    }>();

    function clear() {
        emit('update:modelValue', undefined);
    }
</script>
