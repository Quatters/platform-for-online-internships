export default defineI18nConfig(() => ({
    legacy: false,
    locale: 'ru',
    messages: {
        ru: {
            Id: 'Идентификатор',
            Name: 'Название',
            Description: 'Описание',
            'First name': 'Имя',
            'Last name': 'Фамилия',
            Patronymic: 'Отчество',
            'Is admin': 'Администратор',
            'Is teacher': 'Наставник',
            Email: 'Эл. почта',

            Dashboard: 'Личный кабинет',
            Posts: 'Должности',
            Courses: 'Курсы',
            Subdivisions: 'Подразделения',
            Users: 'Пользователи',

            Create: 'Создать',
            Edit: 'Редактировать',
        },
    },
}));
