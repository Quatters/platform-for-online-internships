import type { ModalButton } from 'node_modules/tailvue';
import type { LocationQueryValue } from 'vue-router';

export const noop = (..._: any) => {};

export const DEFAULT_MODAL_TITLE = 'Подтвердите действие';
export const DEFAULT_SECONDARY_MODAL_BUTTON_OPTIONS: ModalButton = {
    label: 'Отмена',
    action: noop,
    theme: 'text',
};

export function capitalize(value: string) {
    if (!value) {
        return value;
    }
    return value.charAt(0).toUpperCase() + value.slice(1);
}

export function getFirstQueryValue(queryValue: LocationQueryValue | LocationQueryValue[]) {
    let value = queryValue;
    if (Array.isArray(value)) {
        value = value[0];
    }
    return value;
}

export const error404 = () => createError({ fatal: true, statusCode: 404, message: 'Страница не найдена' });

// https://stackoverflow.com/a/2450976
export function shuffle<T>(array: Array<T>): Array<T> {
    let currentIndex = array.length;
    let randomIndex;

    while (currentIndex !== 0) {
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex--;
        [array[currentIndex], array[randomIndex]] = [array[randomIndex], array[currentIndex]];
    }

    return array;
}
