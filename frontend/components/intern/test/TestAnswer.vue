<template>
    <div v-if="type === 'single'">
        <label v-for="(answer, idx) in possibleAnswers" :key="idx" class="block cursor-pointer">
            <input
                type="radio"
                :checked="modelValue === answer.id"
                class="me-1 mb-2"
                @click="(e: Event) => changeSingle(answer.id, (e.target as HTMLInputElement).checked)"
            />
            <span class="inline-block">{{ answer.value }}</span>
        </label>
    </div>
    <div v-else-if="type === 'multiple'">
        <label v-for="(answer, idx) in possibleAnswers" :key="idx" class="block cursor-pointer">
            <input
                type="checkbox"
                :checked="Boolean(modelValue) && (modelValue as number[]).includes(answer.id)"
                class="me-1 mb-2"
                @click="(e: Event) => changeMultiple(answer.id, (e.target as HTMLInputElement).checked)"
            />
            <span class="inline-block">{{ answer.value }}</span>
        </label>
    </div>
    <ControlFormTextArea
        v-else-if="type === 'text'"
        :model-value="(modelValue as string)"
        label=""
        @update:model-value="value => emit('update:modelValue', value)"
    />
</template>

<script setup lang="ts">
    interface PossibleAnswer {
        id: number;
        value: string;
    }

    const props = defineProps<{
        modelValue: string | number | number[] | undefined;
        type: 'single' | 'multiple' | 'text';
        possibleAnswers: PossibleAnswer[] | null | undefined;
    }>();

    const emit = defineEmits<{
        (e: 'update:modelValue', value: typeof props.modelValue): void;
    }>();

    function changeSingle(answerId: number, checked: boolean) {
        if (checked) {
            emit('update:modelValue', answerId);
        }
    }

    function changeMultiple(answerId: number, checked: boolean) {
        const value = props.modelValue ? [...(props.modelValue as number[])] : [];

        if (checked) {
            value.push(answerId);
            emit('update:modelValue', value);
        } else {
            emit(
                'update:modelValue',
                value.filter(key => key !== answerId),
            );
        }
    }
</script>
