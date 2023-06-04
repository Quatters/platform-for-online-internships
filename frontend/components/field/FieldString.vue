<template>
    <div class="whitespace-pre-wrap">
        {{ computedValue }}
    </div>
</template>

<script setup lang="ts">
    import { FieldProps } from '~/types';

    const props = defineProps<FieldProps>();

    const i18n = useI18n();

    const computedValue = computed(() => {
        const v = String(props.value);
        if (i18n.te(v)) {
            return i18n.t(v);
        }
        return v;
    });
</script>
