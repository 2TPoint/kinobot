from telebot.types import ReplyKeyboardMarkup

buttons = ['Поиск', 'Актеры', 'Подборки', 'Случайные фильмы']

dict = {
    'Поиск': ['Назад'],
    'Актеры': ['null', 'null', 'Назад'],
    'Подборки': ['Боевики', 'Драмы', 'Назад'],
    'Случайные фильмы': ['null', 'null', 'Назад']
}

def make_keyboard(str=None):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btns = buttons
    if str is not None:
        btns = dict[str]
    for i in range(len(btns)):
        keyboard.add(btns[i])
    return keyboard