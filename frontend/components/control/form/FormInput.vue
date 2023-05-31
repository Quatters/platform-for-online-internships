<template>
    <div>
        <ControlFormLabel :value="label" :required="required" />
        <input
            :id="label"
            :value="modelValue"
            type="string"
            class="shadow appearance-none border rounded w-full py-2 px-3 border-gray-300 leading-tight focus:outline-none focus:shadow-outline"
            :class="error ? 'border-red-600' : ''"
            :required="required"
            @input="$event => $emit('update:modelValue', ($event.target as HTMLInputElement).value)"
        />
        <div v-if="error" class="text-red-600 mt-2">{{ error }}</div>
    </div>
</template>

<script setup lang="ts">
    defineProps<{
        modelValue?: string;
        label: string;
        error?: string;
        required?: boolean;
    }>();
    defineEmits<{
        (e: 'update:modelValue', value: string): void;
    }>();
</script>
