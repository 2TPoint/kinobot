from kinopoisk.movie import Movie

def get_film(name=None):
    info = Movie(id=278229)
    info.get_content('main_page')
    print(info.year)
    print(info.tagline)
    print(info.rating)