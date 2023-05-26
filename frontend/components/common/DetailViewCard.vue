<template>
    <div class="w-full">
        <div class="bg-white shadow-md rounded-md px-8 py-6">
            <div v-for="([key, value], idx) in Object.entries(item)" :key="idx" class="mb-3">
                <div class="font-medium">
                    {{ $t(capitalize(key.replaceAll('_', ' '))) }}
                </div>
                <FieldAbstract :field-name="key" :value="value" />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    interface Item {
        id: number;
        [key: string]: unknown;
    }

    defineProps<{
        item: Item;
    }>();
</script>
