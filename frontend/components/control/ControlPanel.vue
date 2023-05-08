<template>
    <div class="ms-8 mt-3" :class="$style.buttons">
        <slot name="buttons" />
    </div>
</template>

<style module>
    .buttons > button:not(:first-child) {
        margin-left: 0.5rem;
    }
</style>
