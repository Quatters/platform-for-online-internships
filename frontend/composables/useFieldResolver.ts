import { FieldBoolean, FieldString, FieldArray, FieldObject } from '#components';

export default function () {
    function resolveField(value: unknown) {
        if (typeof value === 'boolean') {
            return FieldBoolean;
        }
        if (Array.isArray(value)) {
            return FieldArray;
        }
        if (typeof value === 'object') {
            return FieldObject;
        }
        return FieldString;
    }

    return {
        resolveField,
    };
}
