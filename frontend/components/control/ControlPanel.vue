<template>
    <div class="mx-8 mt-4 flex justify-between">
        <div class="flex" :class="$style['module-style']">
            <slot name="buttons" />
        </div>

        <div class="flex" :class="$style['module-style']">
            <slot name="links" />
            <slot name="inputs" />
        </div>
    </div>
</template>

<style module lang="scss">
    .module-style {
        & > * {
            text-align: center;
            align-self: center;
        }

        & > *:not(:first-child) {
            margin-left: 0.5rem;
        }
    }
</style>
