<template>
    <div class="px-4 py-3">
        <div class="flex justify-between text-sm">
            <span class="font-medium">{{ getDisplayName(messageObject.sender) }}</span>
            <span>{{ getDisplayDate(messageObject.created_at) }}</span>
        </div>
        <p>
            {{ messageObject.message }}
        </p>
    </div>
</template>

<script setup lang="ts">
    import { components } from '~/openapi';

    const props = defineProps<{
        messageObject: components['schemas']['Message'];
    }>();

    function getDisplayName(user: typeof props.messageObject.sender) {
        return getUserDisplayName(user);
    }

    function getDisplayDate(date: string) {
        return new Date(date).toLocaleString();
    }
</script>
