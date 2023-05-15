<template>
    <ControlButton @click="() => navigateTo({ name: `${String($route.name)}-create` })">Создать</ControlButton>
</template>
