import { defineStore } from 'pinia';
import { components } from '~/openapi';

export default defineStore('test', () => {
    const { $api } = useNuxtApp();
    const test = ref<components['schemas']['GoingTest'] | null | undefined>();
    const answers = ref<Record<number, number | number[] | string>>({});
    const isFetched = ref(false);

    const timerId = ref<ReturnType<typeof setTimeout> | null>(null);
    const seconds = ref<number | null>(null);

    function resetCountdown() {
        if (timerId.value) {
            clearInterval(timerId.value);
            timerId.value = null;
        }
        seconds.value = null;
    }

    function calculateTimeLeft() {
        if (!test.value) {
            return 0;
        }
        const startedAtSeconds = Math.floor(new Date(test.value.started_at).getTime() / 1000);
        const nowSeconds = Math.floor(new Date().getTime() / 1000);
        const spentSeconds = nowSeconds - startedAtSeconds;
        const timeLeft = test.value.time_to_pass - spentSeconds;
        return Math.max(timeLeft, 0);
    }

    function startCountdown() {
        if (!test.value) {
            return;
        }
        resetCountdown();
        seconds.value = calculateTimeLeft();
        if (seconds.value > 0) {
            timerId.value = setInterval(() => {
                seconds.value!--;
            }, 1000);
        }
    }

    function _prependZero(num: number) {
        let strNum = String(num);
        if (strNum.length === 1) {
            strNum = `0${strNum}`;
        }
        return strNum;
    }

    const countdownString = computed(() => {
        if (!seconds.value) {
            return '00:00:00';
        }
        const minutes = Math.floor(seconds.value / 60);
        const _seconds = seconds.value % 60;
        const hours = Math.floor(minutes / 60);
        return `${_prependZero(hours)}:${_prependZero(minutes)}:${_prependZero(_seconds)}`;
    });

    async function fetch({ force }: { force?: boolean } = {}) {
        if (!isFetched.value || force) {
            isFetched.value = true;
            test.value = await $api({
                path: '/api/tests/going',
                method: 'get',
            });
            startCountdown();
        }
    }

    async function startTest({ courseId, topicId }: { courseId: string; topicId: string }) {
        test.value = await $api({
            path: '/api/courses/{course_id}/topics/{topic_id}/start_test',
            method: 'post',
            params: {
                course_id: courseId,
                topic_id: topicId,
            },
        });
        answers.value = {};
        startCountdown();
    }

    function finishTest() {
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
        startTest,
        finishTest,
        fetch,
        test,
        answers,
        countdownString,
    };
});
