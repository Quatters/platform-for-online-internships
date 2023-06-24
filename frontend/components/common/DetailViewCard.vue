<template>
    <div class="w-full">
        <div class="bg-white shadow-md rounded-md px-8 py-6">
            <div v-for="([key, value], idx) in entries" :key="idx" class="mb-3">
                <div class="font-medium">
                    {{ $t(formatValue(key)) }}
                </div>
                <FieldAbstract :field-name="key" :value="value" />
                <slot name="additional-fields" />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    interface Item {
        id: number;
        [key: string]: unknown;
    }

    const props = withDefaults(
        defineProps<{
            item: Item;
            hideFields: Array<string>;
        }>(),
        {
            hideFields: () => [],
        },
    );

    const entries = computed(() => {
        return Object.entries(props.item).filter(([key]) => !props.hideFields.includes(key));
    });

    function formatValue(value: string) {
        return capitalize(value.replaceAll('_', ' '));
    }
</script>
