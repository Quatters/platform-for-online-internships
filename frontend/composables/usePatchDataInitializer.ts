export default function <T extends Record<string, any>>(
    data: Ref<unknown>,
    { m2mFields, fkFields }: { m2mFields?: Array<string>; fkFields?: Array<string> } = {},
) {
    const patchData = ref<T>({} as T);

    watch(
        data,
        value => {
            const _patchData = value as T;
            if (m2mFields) {
                for (const field of m2mFields) {
                    // @ts-expect-error i'm too lazy to solve this
                    _patchData[field] = data.value[field].map(obj => obj.id);
                }
            }
            if (fkFields) {
                for (const field of fkFields) {
                    // @ts-expect-error i'm too lazy to solve this
                    _patchData[`${field}_id`] = data.value[field]?.id;
                }
            }
            // @ts-expect-error i'm too lazy to solve this
            patchData.value = _patchData;
        },
        { immediate: true },
    );

    return {
        patchData,
    };
}
