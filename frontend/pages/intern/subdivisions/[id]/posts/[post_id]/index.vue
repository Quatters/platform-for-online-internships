<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonReturn />
            </template>
        </ControlPanel>
        <CommonContent>
            <InternNameDescriptionCard :name="data!.name" :description="data?.description">
                <template #additional-content>
                    <label class="block py-2 border-t">
                        <span class="inline-block pb-1">Курсы для освоения этой должности</span>
                        <FieldArray :value="data?.courses" field-name="courses" />
                    </label>
                    <label class="block py-2 border-t">
                        <span class="inline-block pb-1">Компетенции, необходимые для этой должности</span>
                        <FieldArray :value="data?.competencies" field-name="competencies" />
                    </label>
                </template>
            </InternNameDescriptionCard>
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const { $api } = useNuxtApp();

    const route = useRoute();
    const pageStore = usePageStore();

    pageStore.fkInstancePathMap = {
        courses: {
            name: 'intern-courses-id',
        },
    };

    const { data } = await useAsyncData(() => {
        return $api({
            path: '/api/subdivisions/{subdivision_id}/posts/{post_id}',
            method: 'get',
            params: { subdivision_id: route.params.id as string, post_id: route.params.post_id as string },
        });
    });
</script>
