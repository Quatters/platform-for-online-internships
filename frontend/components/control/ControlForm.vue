<template>
    <div class="w-full">
        <form ref="form" class="bg-white shadow-md rounded-md px-8 py-6" @submit.stop.prevent="e => $emit('submit', e)">
            <slot />
            <slot name="buttons">
                <ControlButtonSave />
            </slot>
        </form>
    </div>
</template>

<script setup lang="ts">
    defineEmits(['submit']);
</script>
