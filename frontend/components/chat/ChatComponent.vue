<template>
    <div class="w-full h-[calc(100vh-7.2rem)] flex flex-col border border-gray-300 rounded-lg bg-white">
        <div class="flex flex-col justify-between">
            <div class="flex flex-col-reverse overflow-y-auto h-[calc(100vh-10.2rem)]">
                <ChatMessage v-for="item in data?.items" :key="item.id" :message-object="item" />
                <CommonLoadMore :response="data" @load-needed="loadMore" />
            </div>
            <form class="flex bg-gray-200 rounded-b-lg" @submit.prevent="submit()">
                <input
                    v-model="message"
                    placeholder="Введите сообщение..."
                    class="w-full p-3 appearance-none rounded-b-lg rounded-t-none border-t border-gray-300 leading-tight focus:outline-none focus:shadow-outline"
                    :class="{ 'rounded-e-none': message }"
                />
                <ControlButton v-if="message" type="submit" class="rounded-t-none rounded-s-none">
                    Отправить
                </ControlButton>
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
    const props = defineProps<{
        recipientId: number;
    }>();

    const { $api } = useNuxtApp();
    const chatStore = useChatStore();

    const message = ref('');

    const { data, loadMore } = await useListLoader({
        path: '/api/chat/{recipient_id}',
        method: 'get',
        params: {
            recipient_id: props.recipientId,
        },
    });

    chatStore.showNotifications = false;

    onBeforeUnmount(() => (chatStore.showNotifications = true));

    watch(
        toRef(chatStore, 'recentMessage'),
        value => {
            if (value && data.value) {
                data.value.items.unshift(value);
            }
        },
        { immediate: true },
    );

    async function submit() {
        if (!message.value) {
            return;
        }
        await $api({
            path: '/api/chat/{recipient_id}',
            method: 'post',
            params: {
                recipient_id: props.recipientId,
            },
            body: {
                message: message.value,
            },
        });
        message.value = '';
    }
</script>
