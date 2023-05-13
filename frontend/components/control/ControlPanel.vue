<template>
    <div class="mx-8 mt-4" :class="$style.wrapper">
        <slot name="buttons" />
        <slot name="inputs" />
    </div>
</template>

<style module lang="scss">
    .wrapper > button:not(:first-child) {
        margin-left: 0.5rem;
    }
    .wrapper > input:not(:last-child) {
        margin-right: 0.5rem;
    }

    .wrapper > input {
        margin-left: auto;
    }
</style>
