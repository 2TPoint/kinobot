from telebot.types import ReplyKeyboardMarkup

buttons = ['Поиск фильмов', 'Поиск актеров', 'Подборки']

dict = {
    'Поиск фильмов': ['Вернуться в главное меню'],
    'Поиск актеров': ['Назад'],
    'Подборки': ['Топ Популярных Фильмов', 'Топ Самых Лучших Фильмов', 'Триллеры', 'Драмы', 'Страница 2 →', 'Назад'],
    'Страница 1': ['Топ Популярных Фильмов', 'Топ Самых Лучших Фильмов', 'Триллеры', 'Драмы', 'Страница 2 →', 'Назад'],
    'Страница 2': ['Криминал', 'Мелодрамы', "Детективы", "Фантастика", '← Страница 1', 'Страница 3 →'],
    'Страница 3': ['Приключения', 'Биография', "Фильмы-нуары", "Вестерн", '← Страница 2', 'Страница 4 →'],
    'Страница 4': ['Боевики', 'Фэнтези', "Комедии", "Военные", '← Страница 3', 'Страница 5 →'],
    'Страница 5': ['Исторические', 'Ужасы', "Мультфильмы", "Семейные", 'Аниме', '← Страница 4']
}


def make_keyboard(str=None):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btns = buttons
    if str is not None:
        btns = dict[str]
    for i in range(len(btns)):
        keyboard.add(btns[i])
    return keyboard
