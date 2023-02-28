import telebot
from telebot import types

bot = telebot.TeleBot('6144160130:AAGWXCGrnV6rjup9hd4R6FLMc12MfDX6JkA') #инициализируем бота

#обработчик начального сообщения /start
@bot.message_handler(content_types=['text'])
def start(msg):
    if msg.text == '/start':
        keyboard = types.InlineKeyboardMarkup(); #клавиатура для ссылок
        key_github = types.InlineKeyboardButton(text='Наш GitHub', url='https://github.com/2TPoint'); #кнопка GitHub
        keyboard.add(key_github) #добавляем кнопку в клавиатуру
        welcome_text = "Привет! Этот бот создан с целью облегчения поиска информации о киноиндустрии! " \
                       "Бот создан 2TPoint с использованием api Кинопоиска"
        bot.send_message(msg.from_user.id, text=welcome_text, reply_markup=keyboard) #высылаем сообщение

bot.infinity_polling() #бесконечная работа бота