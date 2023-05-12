import type { ModalButton } from 'node_modules/tailvue';

export const noop = () => {};

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
