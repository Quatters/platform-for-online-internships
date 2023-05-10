<template>
    <div class="flex justify-center mt-2">
        <button v-show="canLoad" class="text-blue-700 hover:underline" @click.prevent="loadNeeded">
            Показать больше
        </button>
    </div>
</template>

<script setup lang="ts">
    interface Response {
        items: Array<Record<string, unknown>>;
        total: number;
        limit?: number;
        offset?: number;
    }

    const config = useRuntimeConfig();
    const pageSize = config.public.pageSize;

    const props = defineProps<{
        response?: Response | null;
    }>();

    const canLoad = computed(() => {
        return Boolean(
            props.response &&
                props.response.limit !== undefined &&
                props.response.offset !== undefined &&
                props.response.total > props.response.limit + props.response.offset,
        );
    });

    const emit = defineEmits<{
        (event: 'load-needed', { limit, offset }: { limit: number; offset: number }): void;
    }>();

    function loadNeeded() {
        emit('load-needed', { limit: pageSize, offset: props.response!.offset! + pageSize });
    }
</script>
