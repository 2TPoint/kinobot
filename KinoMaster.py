from kinopoisk_dev import KinopoiskDev

kino_token = open("kino_token.txt").readline()

kp = KinopoiskDev(token=kino_token)

def get_random_films(genre):
    str = kp.find_many_movie()
    print(str)
    return str
