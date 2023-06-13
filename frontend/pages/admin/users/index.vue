<template>
    <div>
        <ControlPanel>
            <template #buttons>
                <ControlButtonCreate />
            </template>
            <template #inputs>
                <ControlFormEnumField
                    v-model="role"
                    nullable
                    :enum-items="['admin', 'teacher', 'intern']"
                    class="w-44"
                />
                <ControlSearchInput v-model="search" />
            </template>
        </ControlPanel>
        <CommonContent>
            <CommonListViewTable :items="data!.items" :hide-fields="['is_admin', 'is_teacher']" />
            <CommonLoadMore :response="data" @load-needed="loadMore" />
        </CommonContent>
    </div>
</template>

<script setup lang="ts">
    const { data, loadMore } = await useListLoader({ path: '/api/users', method: 'get' });

    const route = useRoute();
    const router = useRouter();

    const search = ref<string | null | undefined>(getFirstQueryValue(route.query.search));
    const role = ref<'admin' | 'teacher' | 'intern' | null | undefined>(undefined);

    watch(role, value => {
        router.replace({
            ...route,
            query: {
                ...route.query,
                role: value ?? undefined,
            },
        });
    });
</script>
