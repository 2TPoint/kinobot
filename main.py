import telebot
from telebot import types
from kinopoisk_dev import KinopoiskDev
import KinoMaster
import reply_keyboard

token = open("token.txt").readline()
kino_token = open("kino_token.txt").readline()

bot = telebot.TeleBot(token) #инициализируем бота
kp = KinopoiskDev(token=kino_token)
main_keyboard = reply_keyboard.make_keyboard()
@bot.message_handler(content_types=['text'])
def start(msg):
    global main_keyboard
    # обработчик начального сообщения /start
    if msg.text == '/start':
        keyboard = types.InlineKeyboardMarkup() #клавиатура для ссылок
        key_github = types.InlineKeyboardButton(text='Наш GitHub', url='https://github.com/2TPoint') #кнопка GitHub
        keyboard.add(key_github) #добавляем кнопку в клавиатуру
        welcome_text = "Привет! Этот бот создан с целью облегчения поиска информации о киноиндустрии! " \
                       "Бот создан 2TPoint с использованием api Кинопоиска!!"
        bot.send_message(msg.from_user.id, text=welcome_text, reply_markup=keyboard) #высылаем сообщение
        menu_main(msg)
    if msg.text == 'Подборки':
        menu_collections(msg)
    if msg.text == 'Поиск':
        search(msg)



# метод поиска
def search(msg):
    main_keyboard = reply_keyboard.make_keyboard('Поиск')
    bot.send_message(msg.from_user.id, text="Вы находитесь в меню поиска")
    bot.send_message(msg.from_user.id, text="Введите название фильма/сериала, а я выдам соответствущию информацию о нем", reply_markup=main_keyboard)
    bot.register_next_step_handler(msg, search_engine)

# поиск пока не нажата кнопка назад
def search_engine(msg):
    if msg.text == 'Назад':
        menu_main(msg)
        return
    bot.send_message(msg.from_user.id, text=f"Поиск фильма '{msg.text}'")
    bot.register_next_step_handler(msg, search_engine)

# метод основного меню
def menu_main(msg):
    main_keyboard = reply_keyboard.make_keyboard()
    bot.send_message(msg.from_user.id, text="Вы находитесь в главном меню", reply_markup=main_keyboard)

# метод меню коллекций
def menu_collections(msg):
    main_keyboard = reply_keyboard.make_keyboard('Подборки')
    bot.send_message(msg.from_user.id, text="Меню подборок. Выберите интересующий жанр.",
                     reply_markup=main_keyboard)
    bot.register_next_step_handler(msg, chooseGenre)
    return

# метод выбора жанра для подборок
def chooseGenre(msg):
    if msg.text == 'Назад':
        menu_main(msg)
        return
    bot.send_message(msg.from_user.id, text=f"Вот какие фильмы я нажел по жанру '{msg.text}'")
    text = KinoMaster.get_random_films(msg.text)
    bot.send_message(msg.from_user.id, text=text)
    bot.register_next_step_handler(msg, chooseGenre)

bot.infinity_polling() #бесконечная работа бота