import { defineStore } from 'pinia';
import { components } from '~/openapi';

export default defineStore(
    'chat',
    ({ onNewMessage }: { onNewMessage: (data: components['schemas']['Message']) => void } = { onNewMessage: noop }) => {
        const config = useRuntimeConfig();
        const chatUrl = config.public.apiUrl.split('://').slice(-1);
        const userStore = useUserStore();
        const ws = useWebSocket(`ws://${chatUrl}/api/chat/ws/${userStore.accessToken}`, {
            immediate: false,
            autoClose: false,
            heartbeat: {
                message: '{"ping":true}',
                interval: 5000,
            },
            autoReconnect: {
                retries: 3,
                delay: 3000,
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
                onNewMessage(value);
            },
            { immediate: true },
        );

        return {
            connect,
        };
    },
);
