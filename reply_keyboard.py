import telebot.types
from telebot.types import ReplyKeyboardMarkup

buttons = ['Поиск по фильмам', 'Поиск по актерам', 'Вывести рандомный фильм', 'Подборки']

main_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True
)

def buttons_to_keyboard():
    for i in range(0, len(buttons), 2):
        main_keyboard.row(buttons[i])
        if i+1 < len(buttons):
            main_keyboard.add(buttons[i+1])

def make_keyboard():
    buttons_to_keyboard()
    return main_keyboard