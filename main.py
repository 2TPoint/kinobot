import telebot
from telebot import types
import KinoMaster as km
import reply_keyboard
import parse_film
import parse_actor
from parse_film import *
from parse_actor import *
import wikipedia

token = open("token.txt").readline()
kino_token = open("kino_token.txt").readline()

bot = telebot.TeleBot(token)  # инициализируем бота
main_keyboard = reply_keyboard.make_keyboard()  # клавиатура


# функция апдейтов (оповещение всех пользователей находящихся в БД)
# def update():
#     f = open("db.txt", 'r')
#     for line in f.readlines():
#         id = line
#         bot.send_message(int(id), text='НЕ МУТЬ ПЭЖЭ')
#     f.close()
#
#
# update()

# команда старт
@bot.message_handler(commands=['start'])
def start(msg):
    """
    Обрабатывает команду '/start' от пользователя:
        1. Добавляет id пользователя в базу данных бота
        2. Создает клавиатуру для главного меню
        3. Выводит приветствующий текст

    :param msg: сообщение от пользователя
    :return: ничего не вовзращает
    """
    f = open("db.txt", 'r')
    data = ''
    for line in f.readlines():
        data += line
    f.close()
    if str(msg.from_user.id) not in data:
        f = open("db.txt", 'a')
        f.write(str(msg.from_user.id))
        f.write('\n')
        f.close()
    global main_keyboard
    keyboard = types.InlineKeyboardMarkup()  # клавиатура для ссылок
    key_github = types.InlineKeyboardButton(text='Наш GitHub', url='https://github.com/2TPoint')  # кнопка GitHub
    keyboard.add(key_github)  # добавляем кнопку в клавиатуру
    welcome_text = "Привет! Этот бот создан с целью облегчения поиска информации о киноиндустрии! " \
                   "Бот создан 2TPoint с использованием api Кинопоиска!!"
    bot.send_message(msg.from_user.id, text=welcome_text, reply_markup=keyboard)  # высылаем сообщение
    menu_main(msg)


@bot.message_handler(content_types=['text'])
def main(msg):
    """
    Обрабатывает текст от пользователя, в завимости от текста вызывает соответствующие методы

    :param msg: сообщение от пользователя
    :return: ничего не вовзращает
    """
    if msg.text == 'Актеры':
        search_actor(msg)
    if msg.text == 'Подборки':
        menu_collections(msg)
    if msg.text == 'Поиск':
        search(msg)
    if msg.text == 'Случайные фильмы':
        make_random_film_list(msg)


# метод поиска
def search(msg):
    """
    Выполняет фукнкцию перехода к меню поиска и вызова метода поискового движка

    :param msg: сообщение от пользователя
    :return: ничего не вовзращает
    """
    main_keyboard = reply_keyboard.make_keyboard('Поиск')
    bot.send_message(msg.from_user.id, text="Вы находитесь в меню поиска")
    bot.send_message(msg.from_user.id,
                     text="Введите название фильма/сериала, а я выдам соответствущию информацию о нем",
                     reply_markup=main_keyboard)
    bot.register_next_step_handler(msg, search_engine, 'фильм')


# поиск пока не нажата кнопка назад
def search_engine(msg, type):
    """
    Выполняет финкцию поискового движка, который обрабатывает полученный текст.

    :param msg: сообщение от пользователя
    :param type: тип поиска (фильм/сериал/актер)
    :return: возвращает найденный объект
    """
    message = str(msg.text)
    wikipedia.set_lang("ru")
    if msg.text == 'Назад':
        menu_main(msg)
        return
    if (type == "актер"):
        keyboard = types.InlineKeyboardMarkup()
        print(wikipedia.search(str(msg.text) + ' актер'))
        message = str(msg.text)
        message = message.split(" ")
        message = ' '.join(message[1:]) + ', ' + message[0]
        print(message)
        if (str(message) in wikipedia.search(str(msg.text) + ' актер') or str(wikipedia.search(str(msg.text) + ' актер')[0]).find(message.split(", ")[1])):
            acterURL = PersonURL().getPerson(wikipedia.page(str(msg.text)).url)
            text = acterURL.getName() + '\t' + acterURL.getAge()
            text += '\t' + str(acterURL.getFilms())
            text += '\n' + str(acterURL.getAwards())

            if (len(wikipedia.search(str(msg.text) + ' актер')) > 1):
                wiki = wikipedia.search(str(msg.text) + ' актер')
                for i in range(0, int(len(wiki) / 2 - 1)):
                    keyboard.add(types.InlineKeyboardButton(text=wiki[i], callback_data='acter_' + wiki[i]))

                text += '\n\n' + "Возможно данек\n"
            else:
                keyboard.add(types.InlineKeyboardButton(text="Открыть сайт"))
            bot.send_photo(msg.from_user.id,
                           acterURL.getPicture(),
                           caption=text,
                           reply_markup=keyboard)
        else:
            bot.send_message(msg.from_user.id,
                           text="Некорректный запрос")
    else:
        keyboard = types.InlineKeyboardMarkup()
        print(wikipedia.search(str(msg.text) + ' фильм'))
        if (str(msg.text) in wikipedia.search(str(msg.text) + ' фильм')):
            filmURL = FilmURL().getFilm(wikipedia.page(str(msg.text)).url)
            text = filmURL.getTitle() + '\t' + filmURL.getDate()
            text += '\t' + str(filmURL.getTime())
            text += '\n' + str(filmURL.getActors())
            print(filmURL.getPicture())

            if (len(wikipedia.search(str(msg.text) + ' фильм')) > 1):
                wiki = wikipedia.search(str(msg.text) + ' фильм')
                for i in range(0, int(len(wiki) / 2 - 1)):
                    keyboard.add(types.InlineKeyboardButton(text=wiki[i], callback_data='film_' + wiki[i]))

                text+= '\n\n' + "Также были найдены фильмы\n"
            else:
                keyboard.add(types.InlineKeyboardButton(text="Открыть сайт"))
            bot.send_photo(msg.from_user.id,
                           filmURL.getPicture(),
                            caption=text,
                            reply_markup=keyboard)

        else:
            bot.send_photo(msg.from_user.id,
                           open("img_1.png", 'rb'),
                           caption="Возможно вы имели в виду:\n" +
                        str(wikipedia.search(str(msg.text) + ' фильм')[:5])
                           )
    bot.register_next_step_handler(msg, search_engine, type)


@bot.callback_query_handler(func=lambda call: True)
def ans(call):
    kb = types.InlineKeyboardMarkup()
    cid = call.message.chat.id
    mid = call.message.message_id
    if call.data[:5] == "film_":
        bot.send_message(call.message.chat.id, 'И что дальше?')
        # bot.edit_message_text(chat_id=cid, message_id=mid, text='New Text', reply_markup=kb, parse_mode='Markdown')

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
    text = km.get_random_films(msg.text)
    bot.send_message(msg.from_user.id, text=text)
    bot.register_next_step_handler(msg, chooseGenre)


# метод поиска актеров
def search_actor(msg):
    main_keyboard = reply_keyboard.make_keyboard('Актеры')
    bot.send_message(msg.from_user.id, text="Вы находитесь в меню поиска")
    bot.send_message(msg.from_user.id,
                     text="Введите актера, а я выдам краткую информацию о нем",
                     reply_markup=main_keyboard)
    bot.register_next_step_handler(msg, search_engine, 'актер')


def make_random_film_list(msg):
    s = ''
    movies = km.get_random_films()
    for movie in movies:
        s += movie.title + '\n'

    bot.send_message(msg.from_user.id, text=s)


bot.infinity_polling()  # бесконечная работа бота
