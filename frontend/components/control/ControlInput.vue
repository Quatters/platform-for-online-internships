<template>
    <input
        :placeholder="placeholder"
        :value="modelValue"
        class="bg-white shadow border border-gray-300 text-sm rounded py-2 px-3 transition-all duration-100"
        @input="(e) => onInput((e.target as HTMLInputElement).value)"
    />
</template>

<script setup lang="ts">
    import { useThrottleFn, useDebounceFn } from '@vueuse/core';

    const props = withDefaults(
        defineProps<{
            modelValue?: string | null;
            placeholder?: string;
            throttle?: number;
            debounce?: number;
        }>(),
        {
            placeholder: '',
            throttle: undefined,
            debounce: undefined,
            modelValue: undefined,
        },
    );

    if (props.throttle && props.debounce) {
        throw createError('Passing "throttle" and "debounce" together is ambiguous, choose one.');
    }

    const emit = defineEmits<{
        (e: 'update:modelValue', value: string): void;
    }>();

    function emitInput(value: string) {
        emit('update:modelValue', value);
    }

    const debouncedEmitInput = useDebounceFn(emitInput, props.debounce);
    const throttledEmitInput = useThrottleFn(emitInput, props.throttle);

    function onInput(value: string) {
        if (props.throttle) {
            throttledEmitInput(value);
        } else if (props.debounce) {
            debouncedEmitInput(value);
        } else {
            emitInput(value);
        }
    }
</script>
