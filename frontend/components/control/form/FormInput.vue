<template>
    <div>
        <ControlFormLabel :value="label" :required="required" />
        <input
            :id="label"
            :value="modelValue"
            :type="type"
            class="shadow appearance-none border rounded w-full py-2 px-3 border-gray-300 leading-tight focus:outline-none focus:shadow-outline"
            :class="error ? 'border-red-600' : ''"
            :required="required"
            :max="max"
            :min="min"
            :placeholder="placeholder"
            @input="$event => $emit('update:modelValue', ($event.target as HTMLInputElement).value)"
        />
        <div v-if="error" class="text-red-600 mt-2">{{ error }}</div>
    </div>
</template>

<script setup lang="ts">
    withDefaults(
        defineProps<{
            modelValue?: string | number;
            label: string;
            error?: string;
            required?: boolean;
            type?: string;
            max?: string;
            min?: string;
            placeholder?: string;
        }>(),
        {
            modelValue: '',
            error: '',
            type: 'string',
            max: undefined,
            min: undefined,
            placeholder: '',
        },
    );

    defineEmits<{
        (e: 'update:modelValue', value: string): void;
    }>();
</script>
