<template>
    <CommonContent>
        <div class="w-full h-[calc(100vh-7.2rem)] flex flex-col border border-gray-300 rounded-lg bg-white">
            <div class="p-3 bg-blue-800 text-white rounded-t-lg">
                <span>Чат с наставником</span>
            </div>
            <div class="flex flex-col justify-between h-full">
                <div class="h-[60%]">kek</div>
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
    </CommonContent>
</template>

<script setup lang="ts">
    const userStore = useUserStore();
    const { $api } = useNuxtApp();

    const message = ref('');

    const { data } = useAsyncData(() => {
        return $api({
            path: '/api/chat/{recipient_id}',
            method: 'get',
            params: {
                recipient_id: userStore.user!.teacher!.id,
            },
        });
    });

    function submit() {
        //
    }
</script>
