<template>
    <div class="bg-blue-800 rounded-md flex items-center justify-between px-6 py-4 shadow" :class="$style.statistics">
        <InternDashboardStatisticsItem text="Пройденные курсы" value="2" />
        <InternDashboardStatisticsItem text="Средний балл" value="4.9" />
        <InternDashboardStatisticsItem text="Дней на платформе" value="219" />
        <InternDashboardStatisticsItem text="Место в рейтинге" value="4" />
    </div>
</template>

<style module>
    .statistics > *:not(:first-child) {
        margin-left: 1rem;
    }
</style>
