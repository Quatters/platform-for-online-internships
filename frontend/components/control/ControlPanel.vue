<template>
    <div class="mx-8 mt-4 flex" :class="$style.wrapper">
        <slot name="buttons" />
        <slot name="inputs" />

        <slot name="links" />
    </div>
</template>

<style module lang="scss">
    .wrapper {
        & > button:not(:first-child) {
            margin-left: 0.5rem;
        }

        & > input:not(:last-child) {
            margin-right: 0.5rem;
        }

        & > input {
            margin-left: auto;
            text-align: center;
            align-self: center;
        }

        & > a:not(:last-child) {
            margin-left: auto;
        }

        & > a {
            margin-left: 0.5rem;
            text-align: center;
            align-self: center;
        }
    }
</style>
