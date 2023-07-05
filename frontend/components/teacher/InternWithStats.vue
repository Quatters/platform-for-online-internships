<template>
    <NuxtLink :to="{ name: 'teacher-my_interns-id', params: { id: intern.id } }">
        <CommonCard class="flex justify-between lg:flex-row flex-col hover:bg-gray-100">
            <div class="lg:me-3 lg:mb-0 mb-3 me-0">
                <p class="text-lg font-medium">{{ getDisplayName() }}</p>
                <p>Средний балл: {{ intern.average_score }}</p>
            </div>
            <label v-if="intern.competencies.length" class="block cursor-pointer lg:mx-3 lg:my-0 my-3 mx-0">
                <span class="inline-block mb-1 font-medium">Полученные компетенции:</span>
                <FieldArray field-name="competencies" :value="intern.competencies" />
            </label>
            <label v-if="posts.length" class="block cursor-pointer lg:mx-3 lg:my-0 my-3 mx-0">
                <span class="inline-block mb-1 font-medium">Осваиваемые должности:</span>
                <FieldArray field-name="posts" :value="posts" />
            </label>
            <label v-if="intern.learnt_posts.length" class="block cursor-pointer lg:mx-3 lg:my-0 my-3 mx-0">
                <span class="inline-block mb-1 font-medium">Освоенные должности:</span>
                <FieldArray field-name="learnt_posts" :value="intern.learnt_posts" />
            </label>
            <label v-if="intern.finished_courses.length" class="block cursor-pointer lg:mx-3 lg:my-0 my-3 mx-0">
                <span class="inline-block mb-1 font-medium">Завершенные курсы</span>
                <FieldArray field-name="finished_courses" :value="intern.finished_courses" />
            </label>
        </CommonCard>
    </NuxtLink>
</template>

<script setup lang="ts">
    import { components } from '~/openapi';

    const props = defineProps<{
        intern: components['schemas']['InternWithStats'];
    }>();

    function getDisplayName() {
        return getUserDisplayName(props.intern);
    }

    const posts = computed(() => {
        const learntPostIds = props.intern.posts.map(post => post.id);
        return props.intern.posts.filter(post => !learntPostIds.includes(post.id));
    });
</script>
