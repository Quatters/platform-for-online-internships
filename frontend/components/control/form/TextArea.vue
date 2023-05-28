<template>
    <div>
        <ControlFormLabel :value="label" :required="required" />
        <textarea
            :id="label"
            :value="modelValue"
            type="string"
            class="shadow appearance-none border border-gray-300 rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
            :required="required"
            @input="$event => $emit('update:modelValue', ($event.target as HTMLInputElement).value)"
        />
        <span v-if="error">{{ error }}</span>
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
