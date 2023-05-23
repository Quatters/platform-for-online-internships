<template>
    <component :is="resolveField(value)" :value="value" />
</template>

<script setup lang="ts">
    import { FieldProps } from '~/types';

    defineProps<FieldProps>();

    const { resolveField } = useFieldResolver();
</script>
