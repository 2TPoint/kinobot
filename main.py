import telebot
from telebot import types
from kinopoisk_dev import KinopoiskDev

import reply_keyboard

token = open("token.txt").readline()
kino_token = open("kino_token.txt").readline()

bot = telebot.TeleBot(token) #инициализируем бота
kp = KinopoiskDev(token=kino_token)
main_keyboard = reply_keyboard.make_keyboard()
@bot.message_handler(content_types=['text'])
def start(msg):
    # обработчик начального сообщения /start
    if msg.text == '/start':
        keyboard = types.InlineKeyboardMarkup() #клавиатура для ссылок
        key_github = types.InlineKeyboardButton(text='Наш GitHub', url='https://github.com/2TPoint') #кнопка GitHub
        keyboard.add(key_github) #добавляем кнопку в клавиатуру
        welcome_text = "Привет! Этот бот создан с целью облегчения поиска информации о киноиндустрии! " \
                       "Бот создан 2TPoint с использованием api Кинопоиска!!"
        bot.send_message(msg.from_user.id, text=welcome_text, reply_markup=keyboard) #высылаем сообщение
        bot.send_message(msg.from_user.id, reply_markup=main_keyboard, text="Вы находитесь в главном меню")

bot.infinity_polling() #бесконечная работа бота