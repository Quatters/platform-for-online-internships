<template>
    <button
        class="px-4 py-2 rounded-md text-sm transition-colors duration-100 disabled:bg-gray-400 disabled:text-gray-50"
        :class="computedClass"
        :disabled="disabled"
        @click="$emit('click')"
    >
        <slot />
    </button>
</template>

<script setup lang="ts">
    interface Props {
        class?: string;
        variant?: 'blue' | 'gray' | 'red';
        disabled?: boolean;
    }
    const variants: Record<NonNullable<Props['variant']>, string> = {
        blue: 'bg-blue-800 hover:bg-blue-700 text-white',
        gray: 'bg-gray-500 hover:bg-gray-400 text-white',
        red: 'bg-red-600 hover:bg-red-500 text-white',
    };
    const props = withDefaults(defineProps<Props>(), {
        variant: 'blue',
        class: '',
        disabled: false,
    });

    const computedClass = computed(() => {
        return `${props.class} ${variants[props.variant]}`;
    });

    defineEmits(['click']);
</script>
