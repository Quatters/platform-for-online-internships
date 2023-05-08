<template>
    <button
        class="px-4 py-2 rounded-md text-sm transition-colors duration-100"
        :class="computedClass"
        @click="$emit('click')"
    >
        <slot />
    </button>
</template>

<script setup lang="ts">
    interface Props {
        class?: string;
        variant?: 'blue' | 'gray' | 'red';
    }
    const variants: Record<NonNullable<Props['variant']>, string> = {
        blue: 'bg-blue-800 hover:bg-blue-700 text-white',
        gray: 'bg-gray-600 hover:bg-gray-500 text-white',
        red: 'bg-red-700 hover:bg-red-600 text-white',
    };
    const props = withDefaults(defineProps<Props>(), {
        variant: 'blue',
        class: '',
    });

    const computedClass = computed(() => {
        return `${props.class} ${variants[props.variant]}`;
    });

    defineEmits(['click']);
</script>
