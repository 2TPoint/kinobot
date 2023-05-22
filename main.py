import telebot
from telebot import types
import KinoMaster as km
import reply_keyboard
import parse_film
import parse_actor
from parse_film import *
from parse_actor import *
import wikipedia
from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.film_top_request import FilmTopRequest
from kinopoisk_unofficial.model.dictonary.top_type import TopType
# Для вызова корутины main вам нужно создать событийный цикл и запустить его
import asyncio
from urllib.parse import quote

class MiniFilm:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def getId(self):
        return self.id

    def getName(self):
        return self.name

class MiniActor:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def getId(self):
        return self.id

    def getName(self):
        return self.name


page = 1

token = open("token.txt").readline()
kino_token = open("kino_token.txt").readline()

api_client = KinopoiskApiClient("b6e6a2c3-d103-49c0-97f4-414963a75e13")

bot = telebot.TeleBot(token)  # инициализируем бота
main_keyboard = reply_keyboard.make_keyboard()  # клавиатура

actor_films = 0


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
    if msg.text == 'Поиск актеров':
        search_actor(msg)
    if msg.text == 'Подборки':
        menu_collections(msg)
    if msg.text == 'Поиск фильмов':
        search(msg)


# метод поиска
def search(msg):
    """
    Выполняет фукнкцию перехода к меню поиска и вызова метода поискового движка

    :param msg: сообщение от пользователя
    :return: ничего не вовзращает
    """
    main_keyboard = reply_keyboard.make_keyboard('Поиск фильмов')
    bot.send_message(msg.from_user.id, text="Вы находитесь в меню поиска")
    bot.send_message(msg.from_user.id,
                     text="Введите название фильма/сериала или актера, играющего роль в фильме, а я выдам соответствущию информацию о нем",
                     reply_markup=main_keyboard)
    bot.register_next_step_handler(msg, search_engine, 'фильм')

search_text = ""

# поиск пока не нажата кнопка назад
@bot.message_handler(content_types=['text'])
def search_engine(msg, type):
    """
    Выполняет финкцию поискового движка, который обрабатывает полученный текст.

    :param msg: сообщение от пользователя
    :param type: тип поиска (фильм/сериал/актер)
    :return: возвращает найденный объект
    """
    global page
    page = 1
    if (msg.text == 'Вернуться в главное меню'):
        menu_main(msg)
        return
    global search_text
    search_text = msg.text
    search_text = quote(search_text)
    url = f'https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword?keyword={search_text}&page={page}'
    keyboard = FilmsInline(url)
    if (len(keyboard.keyboard) == 20):
        keyboard.add(types.InlineKeyboardButton(text="Следующая →", callback_data="next_search"))
    if (page > 1):
        keyboard.add(types.InlineKeyboardButton(text="← Предыдущая", callback_data="prev_search"))
    if (len(keyboard.keyboard) >= 1):
        bot.send_message(msg.from_user.id, text=f"Вот какие фильмы я нашел по запросу '{msg.text}'", reply_markup=keyboard)
    else:
        bot.send_message(msg.from_user.id, text=f"К сожалению, не удалось найти фильмов, соответствующих запросу \"{msg.text}\". Рекомендуется повторно проверить название фильма и попробовать снова.")
    bot.register_next_step_handler(msg, search_engine, type)


@bot.callback_query_handler(func=lambda call: True)
def ans(call):
    kb = types.InlineKeyboardMarkup()
    cid = call.message.chat.id
    mid = call.message.message_id
    global page  # Extract current page number
    global actor_films
    if call.data == 'next_top_100':
        page += 1  # Increment page number
        keyboard = FilmsInline(f"https://kinopoiskapiunofficial.tech/api/v2.2/films/top?type=TOP_100_POPULAR_FILMS&page={page}")
        if (page > 1):
            keyboard.add(types.InlineKeyboardButton(text="← Предыдущая", callback_data="prev_top_100"))
        if (len(keyboard.keyboard) >= 20):
            keyboard.add(types.InlineKeyboardButton(text="Следующая →", callback_data="next_top_100"))
        bot.edit_message_reply_markup(chat_id=cid, message_id=mid, reply_markup=keyboard)

    if call.data == 'prev_top_100':
        page -= 1  # Increment page number
        keyboard = FilmsInline(f"https://kinopoiskapiunofficial.tech/api/v2.2/films/top?type=TOP_100_POPULAR_FILMS&page={page}")
        if (page > 1):
            keyboard.add(types.InlineKeyboardButton(text="← Предыдущая", callback_data="prev_top_100"))
        if (len(keyboard.keyboard) >= 20):
            keyboard.add(types.InlineKeyboardButton(text="Следующая →", callback_data="next_top_100"))
        bot.edit_message_reply_markup(chat_id=cid, message_id=mid, reply_markup=keyboard)

    if call.data == 'next_search':
        page += 1  # Increment page number
        keyboard = FilmsInline(f'https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword?keyword={search_text}&page={page}')
        if (page > 1):
            keyboard.add(types.InlineKeyboardButton(text="← Предыдущая", callback_data="prev_search"))
        if (len(keyboard.keyboard) >= 20):
            keyboard.add(types.InlineKeyboardButton(text="Следующая →", callback_data="next_search"))
        bot.edit_message_reply_markup(chat_id=cid, message_id=mid, reply_markup=keyboard)

    if call.data == 'prev_search':
        page -= 1  # Increment page number
        keyboard = FilmsInline(f'https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword?keyword={search_text}&page={page}')
        if (page > 1):
            keyboard.add(types.InlineKeyboardButton(text="← Предыдущая", callback_data="prev_search"))
        if (len(keyboard.keyboard) >= 20):
            keyboard.add(types.InlineKeyboardButton(text="Следующая →", callback_data="next_search"))
        bot.edit_message_reply_markup(chat_id=cid, message_id=mid, reply_markup=keyboard)

    if str(call.data).find("movie_id_") != -1:
        id = str(call.data).replace("movie_id_", "")
        showFilm(id, cid)
    if str(call.data).find("actor_id_") != -1:
        id = str(call.data).replace("actor_id_", "")
        showActor(id, cid)
    if str(call.data).find("similar_films_") != -1:
        id = str(call.data).replace("similar_films_", "")
        ShowSimilarFilms(id, cid)
    if str(call.data).find("next_5_films_actor_") != -1:
        actor_films += 5
        id = str(call.data).replace("next_5_films_actor_", "")
        EditActorFilms(id, cid, mid)
    if str(call.data).find("prev_5_films_actor_") != -1:
        actor_films -= 5
        id = str(call.data).replace("prev_5_films_actor_", "")
        EditActorFilms(id, cid, mid)

def showFilm(id, cid):
    url = f'https://kinopoiskapiunofficial.tech/api/v2.2/films/{id}'
    movie = getMovies(url)
    keyboard = types.InlineKeyboardMarkup()
    img_data = requests.get(movie['posterUrlPreview']).content
    with open('film_poster.png', 'wb') as handler:
        handler.write(img_data)
    name = movie['nameRu']
    year = movie['year']
    filmLength = movie['filmLength']
    if (filmLength is not None):
        hours = int(filmLength) // 60  # Целочисленное деление на 60 даст количество часов
        remaining_minutes = int(filmLength) % 60  # Остаток от деления на 60 даст количество оставшихся минут
        # Форматирование результата в виде "часы:минуты"
        filmLength = "{:02d}:{:02d}".format(hours, remaining_minutes)
    countries = movie['countries']
    genres = movie['genres']
    rating = movie['ratingKinopoisk']
    ratingVoteCount = movie['ratingKinopoiskVoteCount']
    description = movie['description']
    slogan = movie['slogan']
    webUrl = movie['webUrl']

    info = f"{name} ({year}), {rating} ⭐️ ({ratingVoteCount} оценок)\n" \
            f"\n🎥 О фильме 🎥\n\n" \
            f"📅 Год производства {year}\n"
    info += "\n🌍 Страна: "
    for country in countries:
        info += country['country']
        if (list(countries).index(country) != len(list(countries)) - 1):
            info += ', '
    info += f"\n\n🎬 Жанр: "
    for genre in genres:
        info += genre['genre']
        if (list(genres).index(genre) != len(list(genres)) - 1):
            info += ', '
    info += '\n'
    if (slogan != 'None'):
        info += f"\n💬 Слоган: \'{slogan}\'\n"
    info += f"\n⏰ Время {filmLength}\n"

    key_open_kinopoisk = types.InlineKeyboardButton(text='Фильм на КиноПоиске', url=webUrl)
    key_show_similar = types.InlineKeyboardButton(text='Похожие Фильмы', callback_data="similar_films_"+str(movie['kinopoiskId']), parse_mode="Markdown")
    keyboard.add(key_show_similar)  # добавляем кнопку в клавиатуру
    keyboard.add(key_open_kinopoisk)  # добавляем кнопку в клавиатуру

    if (description is None):
        description = "Синопсис отсутствует"
    if (len(info + f"\n" + f"\n📜 Синопсис\n" + description) < 1000):
        info += f"\n" + f"\n📜 Синопсис\n" + description
        bot.send_photo(chat_id=cid, photo=open("film_poster.png", 'rb'), caption=info, reply_markup=keyboard)
    else:
        msg = bot.send_photo(chat_id=cid, photo=open("film_poster.png", 'rb'), caption=info,
                            reply_markup=keyboard)
        bot.reply_to(msg, text=f"\n" + f"\n📜 Синопсис\n" + description)


def ShowSimilarFilms(id, cid):
    url = f'https://kinopoiskapiunofficial.tech/api/v2.2/films/{id}/similars'
    keyboard = FilmsInline(url)
    bot.send_photo(chat_id=cid, photo=open("film_poster.png", 'rb'), caption="Подборка похожих фильмов", reply_markup=keyboard)


# метод основного меню
def menu_main(msg):
    main_keyboard = reply_keyboard.make_keyboard()
    bot.send_message(msg.from_user.id, text="Вы находитесь в главном меню", reply_markup=main_keyboard)
    keyboard = types.InlineKeyboardMarkup()

# метод меню коллекций
def menu_collections(msg):
    main_keyboard = reply_keyboard.make_keyboard('Подборки')
    bot.send_message(msg.from_user.id, text="Меню подборок. Выберите интересующий жанр.",
                     reply_markup=main_keyboard)
    bot.register_next_step_handler(msg, chooseGenre)
    return


def getMovies(url):
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": "b6e6a2c3-d103-49c0-97f4-414963a75e13",
    }
    resp = requests.get(url, headers=headers)
    respData = resp.json()
    return respData


def dict_to_list(films_dict, isTop):
    films_list = []
    if (dict(films_dict).keys().__contains__('films')):
        for film in films_dict['films']:
            film = dict(film)
            film_rating = str(film['rating'])
            if film_rating.rfind('%') != -1 and isTop == True:
                pass
            else:
                film_name = ""
                if (dict(film).keys().__contains__('nameRu')):
                    film_name = film['nameRu']
                else:
                    film_name = film['nameEn']
                film_year = film['year']
                film_info = f"{film_name} ({film_year}), {film_rating} ☆"
                mini = MiniFilm(film['filmId'], film_info)
                films_list.append(mini)
    else:
        for film in films_dict['items']:
            if ((dict(film).keys().__contains__('sex'))):
                actor_name = film['nameRu']
                if ((dict(film).keys().__contains__('kinopoiskId'))):
                    mini = MiniActor(film['kinopoiskId'], actor_name)
                else:
                    mini = MiniActor(film['personId'], actor_name)
                films_list.append(mini)
            else:
                film_name = film['nameRu']
                if ((dict(film).keys().__contains__('filmId'))):
                    mini = MiniFilm(film['filmId'], film_name)
                else:
                    mini = MiniFilm(film['kinopoiskId'], film_name)
                films_list.append(mini)
    return films_list


def FilmsInline(url, isTop=False, isMovie=True):
    keyboard = types.InlineKeyboardMarkup()
    if (isMovie):
        array = dict_to_list(getMovies(url), isTop)
        for movie in array:
            keyboard.add(types.InlineKeyboardButton(text=movie.getName(), callback_data='movie_id_' + str(movie.getId())))
    else:
        array = dict_to_list(getActors(url), False)
        for actor in array:
            keyboard.add(types.InlineKeyboardButton(text=actor.getName(), callback_data='actor_id_' + str(actor.getId())))
    return keyboard


# метод выбора жанра для подборок
def chooseGenre(msg):
    global main_keyboard
    global page
    page = 1
    if msg.text == 'Назад':
        menu_main(msg)
        return
    if str(msg.text).find('→') != -1 or str(msg.text).find('←') != -1:
        text = str(msg.text)
        if text.find(' →') != -1:
            text = text.replace(" →", "")
        if text.find('← ') != -1:
            text = text.replace("← ", "")
        main_keyboard = reply_keyboard.make_keyboard(text)
        text = text.replace("Страница", "")
        bot.send_message(msg.from_user.id, text="Вы перешли на страницу " + text,
                         reply_markup=main_keyboard)
    else:
        url = ""
        img = ""
        if (msg.text == "Топ Популярных Фильмов"):
            url = f"https://kinopoiskapiunofficial.tech/api/v2.2/films/top?type=TOP_100_POPULAR_FILMS&page={page}"
            img = "top100.png"
        if (msg.text == "Топ Самых Лучших Фильмов"):
            url = f"https://kinopoiskapiunofficial.tech/api/v2.2/films/top?type=TOP_250_BEST_FILMS&page={page}"
            img = "top250.png"
        else:
            img = "genres_img.png"
            genre_pos = getGenrePos(msg.text)
            url = f"https://kinopoiskapiunofficial.tech/api/v2.2/films?genres={genre_pos}&order=RATING&type=ALL&ratingFrom=0&ratingTo=10&yearFrom=1000&yearTo=3000&page={page}"
        keyboard = FilmsInline(url, True)
        keyboard.add(types.InlineKeyboardButton(text="Следующая →", callback_data="next_top_100"))
        bot.send_photo(msg.from_user.id, open(img, 'rb'),
                       caption=f"Вот какие фильмы я нашел по подборке '{msg.text}'", reply_markup=keyboard)
    bot.register_next_step_handler(msg, chooseGenre)

def getGenrePos(text):
    set = {
    'Триллеры':1,
    'Драмы':2,
    'Криминал':3,
    'Мелодрамы':4,
    'Детективы':5,
    'Фантастика':6,
    'Приключения':7,
    'Биография':8,
    'Фильмы-нуары':9,
    'Вестерн':10,
    'Боевики':11,
    'Фэнтези':12,
    'Комедии':13,
    'Военные':14,
    'Исторические':15,
    'Ужасы':17,
    'Мультфильмы':18,
    'Семейные':19,
    'Аниме':24
    }
    return set[text]

def getActors(url):
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": "b6e6a2c3-d103-49c0-97f4-414963a75e13",
    }
    resp = requests.get(url, headers=headers)
    respData = resp.json()
    return respData

def EditActorFilms(id, cid, mid):
    global actor_films
    url = f'https://kinopoiskapiunofficial.tech/api/v1/staff/{id}'
    actor = getActors(url)
    keyboard = types.InlineKeyboardMarkup()
    films = actor['films']
    for i in range(actor_films, actor_films + 5):
        if (actor_films % 5 == 0):
            break
        mini = MiniFilm(films[i]['filmId'], films[i]['nameRu'])
        key_show_films = types.InlineKeyboardButton(text=str(mini.getName()),
                                                      callback_data="movie_id_" + str(mini.getId()),
                                                      parse_mode="Markdown")
        keyboard.add(key_show_films)

    if (actor_films >= 5):
        key_prev_films = types.InlineKeyboardButton(text='← Предыдущая',
                                                    callback_data="prev_5_films_actor_" + str(actor['personId']))
        keyboard.add(key_prev_films)

    if (actor_films != len(list(films))):
        key_next_films = types.InlineKeyboardButton(text='Следующая →', callback_data="next_5_films_actor_" + str(actor['personId']))
        keyboard.add(key_next_films)

    key_open_kinopoisk = types.InlineKeyboardButton(text='Страница на КиноПоиске', url=actor['webUrl'])
    keyboard.add(key_open_kinopoisk)  # добавляем кнопку в клавиатуру

    bot.edit_message_reply_markup(chat_id=cid, message_id=mid, reply_markup=keyboard)

def showActor(id, cid):
    global actor_films
    actor_films = 0
    url = f'https://kinopoiskapiunofficial.tech/api/v1/staff/{id}'
    actor = getActors(url)
    keyboard = types.InlineKeyboardMarkup()
    img_data = requests.get(actor['posterUrl']).content
    with open('actor_poster.png', 'wb') as handler:
        handler.write(img_data)
    name = actor['nameRu']
    age = actor['age']
    birthplace = actor['birthplace']
    birthday = actor['birthday']
    facts = actor['facts']
    films = actor['films']
    profession = actor['profession']
    facts_str = ""
    for fact in facts:
        facts_str += fact
        if (list(facts).index(fact) != len(list(facts)) - 1):
            facts_str += ',\n'

    if (profession is None):
        profession = "Неизвестно"
    webUrl = actor['webUrl']
    info = f"{name} ({age} лет)\n" \
           f"💼 Карьера: {profession} \n\n" \
           f"📅 День рождения {birthday} ({birthplace}, {age} лет)\n" \

    key_open_kinopoisk = types.InlineKeyboardButton(text='Страница на КиноПоиске', url=webUrl)

    for film in films:
        if (actor_films > 5):
            break
        mini = MiniActor(film['filmId'], film['nameRu'])
        key_show_films = types.InlineKeyboardButton(text=str(mini.getName()),
                                                      callback_data="movie_id_" + str(mini.getId()),
                                                      parse_mode="Markdown")
        actor_films += 1
        keyboard.add(key_show_films)

    if (actor_films > 5):
        key_next_films = types.InlineKeyboardButton(text='Следующая →', callback_data="next_5_films_actor_" + str(actor['personId']))
        keyboard.add(key_next_films)

    keyboard.add(key_open_kinopoisk)  # добавляем кнопку в клавиатуру

    if (facts_str is None):
        facts_str = "-"
    if (len(info + f"\n" + f"\n💡 Интересные факты\n" + facts_str) < 1000):
        if (facts_str != '-'):
            info += f"\n" + f"\n💡 Интересные факты\n" + facts_str
        bot.send_photo(chat_id=cid, photo=open("actor_poster.png", 'rb'), caption=info, reply_markup=keyboard)
    else:
        msg = bot.send_photo(chat_id=cid, photo=open("actor_poster.png", 'rb'), caption=info, reply_markup=keyboard)
        if (facts_str != '-'):
            bot.reply_to(msg, text=f"\n" + f"\n💡 Интересные факты\n" + facts_str)

# метод поиска актеров
@bot.message_handler(content_types=['text'])
def search_actor(msg):
    main_keyboard = reply_keyboard.make_keyboard('Поиск актеров')
    bot.send_message(msg.from_user.id, text="Поиск актеров по ключевым словам. Введите актера, которого вы ходите найти.",reply_markup=main_keyboard)
    bot.register_next_step_handler(msg, search_actor_going)

@bot.message_handler(content_types=['text'])
def search_actor_going(msg):
    if (msg.text == 'Назад'):
        menu_main(msg)
        return
    name = quote(msg.text)
    url = f'https://kinopoiskapiunofficial.tech/api/v1/persons?name={name}&page=1'
    keyboard = FilmsInline(url, False, False)
    if (len(keyboard.keyboard) >= 1):
        bot.send_message(msg.from_user.id, text=f"Результат поиска актеров по запросу: \'{msg.text}\'",
                         reply_markup=keyboard)
    else:
        bot.send_message(msg.from_user.id, text=f"По запросу: \'{msg.text}\' не было найдено ни одного актера.")
    bot.register_next_step_handler(msg, search_actor_going)

def make_random_film_list(msg):
    s = ''
    movies = km.get_random_films()
    for movie in movies:
        s += movie.title + '\n'
    bot.send_message(msg.from_user.id, text=s)


bot.infinity_polling()  # бесконечная работа бота
