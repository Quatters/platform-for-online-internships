<template>
    <ControlButton @click="$emit('save')">Сохранить</ControlButton>
</template>

<script setup lang="ts">
    defineEmits(['save']);
</script>
