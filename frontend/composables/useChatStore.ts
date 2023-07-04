import { RouteLocationRaw } from 'vue-router';
import { defineStore } from 'pinia';
import { components } from '~/openapi';

export default defineStore('chat', () => {
    const config = useRuntimeConfig();
    const chatUrl = config.public.apiUrl.split('://').slice(-1);
    const userStore = useUserStore();
    const showNotifications = ref(false);
    const { $toast } = useNuxtApp();
    const recentMessage = ref<components['schemas']['Message']>();

    const ws = useWebSocket(`ws://${chatUrl}/api/chat/ws/${userStore.accessToken}`, {
        immediate: false,
        heartbeat: {
            interval: 10000,
            message: 'ping',
            pongTimeout: 10000,
        },
        autoReconnect: {
            retries: 20,
            delay: 10000,
            onFailed() {
                console.error('Failed to connect to chat.');
            },
        },
    });

    function connect({ force }: { force?: boolean } = {}) {
        if (ws.status.value === 'CLOSED' || force) {
            ws.open();
        }
    }

    watch(
        ws.data,
        value => {
            let data;
            try {
                data = JSON.parse(value);
            } catch {
                return;
            }
            if (data && 'message' in data && 'sender' in data) {
                recentMessage.value = data;
                if (showNotifications.value) {
                    let link: RouteLocationRaw = { name: 'intern-chat' };
                    if (userStore.user?.is_teacher) {
                        link = { name: 'teacher-my_interns-id-chat', params: { id: data.sender.id } };
                    }
                    $toast.show({
                        message: `${getUserDisplayName(data.sender)}: ${data.message}`,
                        timeout: 4,
                        type: 'info',
                        primary: {
                            action: () => navigateTo(link),
                            label: 'Перейти в чат',
                        },
                    });
                }
            }
        },
        { immediate: true },
    );

    return {
        connect,
        showNotifications,
        recentMessage,
    };
});
