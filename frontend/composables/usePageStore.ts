import { defineStore } from 'pinia';

export default defineStore('page', () => {
    const name = ref('');

    return {
        name,
    };
});
