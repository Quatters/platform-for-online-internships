<template>
    <ControlButton @click="() => navigateTo({ name: `${String($route.name)}-edit` })">Редактировать</ControlButton>
</template>
