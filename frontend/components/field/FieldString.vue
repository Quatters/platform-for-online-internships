<template>
    <div class="whitespace-pre-wrap">
        {{ value }}
    </div>
</template>

<script setup lang="ts">
    import { FieldProps } from '~/types';

    defineProps<FieldProps>();
</script>
