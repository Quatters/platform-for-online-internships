<template>
    <input type="checkbox" :checked="typedValue" disabled />
</template>

<script setup lang="ts">
    import { FieldProps } from '~/types';

    const props = defineProps<FieldProps>();

    const typedValue = ref<boolean>(props.value as boolean);
</script>
