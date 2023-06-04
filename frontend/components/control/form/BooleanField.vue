<template>
    <div class="flex">
        <input
            :id="label"
            type="checkbox"
            :checked="Boolean(modelValue)"
            class="cursor-pointer"
            @change="() => setValue(!modelValue)"
        />
        <ControlFormLabel :value="label" :required="required" class="cursor-pointer !m-0 !ms-2" />
    </div>
</template>

<script setup lang="ts">
    const props = withDefaults(
        defineProps<{
            modelValue?: boolean | undefined | null;
            required?: boolean;
            label: string;
        }>(),
        {
            modelValue: false,
            required: false,
        },
    );

    const emit = defineEmits<{
        (e: 'update:modelValue', value: typeof props.modelValue): void;
    }>();

    function setValue(value: boolean) {
        emit('update:modelValue', value);
    }
</script>
