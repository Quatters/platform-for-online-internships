import { FieldBoolean, FieldString, FieldArray } from '#components';

export default function () {
    function resolveField(value: unknown) {
        if (typeof value === 'boolean') {
            return FieldBoolean;
        }
        if (Array.isArray(value)) {
            return FieldArray;
        }
        return FieldString;
    }

    return {
        resolveField,
    };
}
