import requests
from bs4 import BeautifulSoup


class FilmURL:
    default_url = 'https://ru.wikipedia.org/wiki/'

    class __Film():
        def isExist(self):
            if self.__bs4URL is None:
                return False
            else:
                return True
        def __init__(self, url):
            if requests.get(url).status_code != 404:
                self.__bs4URL = BeautifulSoup(requests.get(url).text,'html.parser')
            else:
                self.__bs4URL = None

        def getTitle(self):
            try:
                return self.__bs4URL.find(class_='infobox-above').text
            except Exception:
                return ""

        def getCategory(self):
            try:
                all = self.__bs4URL.find_all('span', class_='no-wikidata')
                genres = set()
                for i in all:
                    if str(i).__contains__("P136"):
                        for genre in i:
                            if genre.text != '': genres.add(genre.text)
                        break
                return list(genres)
            except Exception:
                return list()

        def getActors(self):
            try:
                all = self.__bs4URL.find_all('span', class_='no-wikidata')
                actors = set()
                for i in all:
                    if str(i).__contains__("P161"):
                        for actor in i:
                            if actor.text != '': actors.add(actor.text)
                        break
                return list(actors)
            except Exception:
                return list()

        def getDirector(self):
            try:
                all = self.__bs4URL.find_all('span', class_='no-wikidata')
                for i in all:
                    if str(i).__contains__("P57"):
                        for director in i:
                            if director.text != '': return director.text
            except Exception:
                return ""

        def getTime(self):
            try:
                all = self.__bs4URL.find_all('span', class_='no-wikidata')
                for i in all:
                    if str(i).__contains__("P2047"):
                        for director in i:
                            if director.text != '': return director.text
            except Exception:
                return ""

        def getDate(self):
            try:
                return self.__bs4URL.find('span', class_='nowrap').text + " год"
            except:
                return ""

        def getMoreInformation(self):
            try:
                a = str(self.__bs4URL.find('a', class_='external text'))
                a = a[a.find('=') + 2:]
                a = a[a.find('=') + 2:]
                a = a[:a.find('"')]
                return a
            except Exception:
                return ""

        def getPicture(self):
            try:
                s = self.__bs4URL.find_all('img')
                for photo in s:
                    a = str(photo)
                    if a.__contains__("Постер фильма"):
                        s = str(photo)
                        s = s[s.find('src') + 5:]
                        s = s[:s.find(' ') - 1]
                        return "https:" + s
            except Exception:
                return ""

    def getFilm(self, title):
        return self.__Film(title)
