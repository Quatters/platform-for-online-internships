import { defineStore } from 'pinia';
import { components } from '~/openapi';

export default defineStore('going-test', () => {
    const { $api } = useNuxtApp();
    const test = ref<components['schemas']['GoingTest'] | null | undefined>();
    const answers = ref<Record<number, number | number[] | string>>({});
    const isFetched = ref(false);

    async function fetch({ force }: { force?: boolean } = {}) {
        if (!isFetched.value || force) {
            isFetched.value = true;
            test.value = await $api({
                path: '/api/tests/going',
                method: 'get',
            });
        }
    }

    function finish() {
        if (!test.value) {
            return;
        }
        return $api({
            path: '/api/tests/{test_id}/finish',
            method: 'post',
            params: {
                test_id: test.value.id,
            },
            body: Object.entries(answers.value).map(([key, value]) => ({ task_id: key, answer: value })),
        });
    }

    return {
        fetch,
        test,
        finish,
        answers,
    };
});
