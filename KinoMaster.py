from kinopoisk.movie import Movie


def get_film(name=None):
    id = Movie.objects.search(name)
    mov = []
    for m in id:
        if m.votes is not None:
            mov.append(m)
    movie = mov[0]
    print(movie)
    print(movie.id)
    try:
        movie.get_content('main_page')
    except Exception:
        pass
    print(movie.plot)
    return None


def testfilms():
    titles = ['Inception', 'Avatar', 'Game of Thrones', 'God Father']
    for title in titles:
        print(get_film(title))


testfilms()
