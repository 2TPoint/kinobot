import requests
from bs4 import BeautifulSoup


class PersonURL:
    class __Person:
        def isExist(self):
            if self.__bs4URL is None:
                return False
            else:
                return True
        __months = ['января', 'февраля', 'марта', 'апреля', 'мая',
                    'июня', 'июля', 'августа', 'сентября', 'октября',
                    'ноября', 'декабря']

        def __init__(self, url):
            if requests.get(url).status_code != 404:
                self.__bs4URL = BeautifulSoup(requests.get(url).text, 'html.parser')
            else:
                self.__bs4URL = None

        def getPicture(self):
            try:
                s = str(self.__bs4URL.find('img'))
                s = s[s.find('src') + 5:]
                s = s[:s.find(' ') - 1]
                return "https:" + s
            except Exception:
                return "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Flag_of_Russia.svg/20px-Flag_of_Russia.svg.png"

        def getName(self):
            try:
                return self.__bs4URL.find('th', class_='infobox-above').text
            except Exception:
                return ""

        def getAge(self):
            try:
                date = self.__bs4URL.find('span', class_='bday').text
                day = date[date.rfind('-') + 1:]
                index = int(date[5:date.rfind('-')])
                month = self.__months[index - 1]
                year = date[:date.find('-')]
                bday = day + " " + month + " " + year
                if self.__bs4URL.find('span', class_='nowrap').text != bday:
                    return bday + " " + self.__bs4URL.find('span', class_='nowrap').text
                else:
                    return day + " " + month + " " + year
            except Exception:
                return ""

        def getFilms(self):
            try:
                all_films = self.__bs4URL.find_all('a')
                films = set()
                for i in all_films:
                    if str(i).__contains__('(фильм)'):
                        films.add(i.text)
                return list(films)
            except Exception:
                return list()

        def getAwards(self):
            try:
                all = self.__bs4URL.find_all('span', class_='no-wikidata')
                awards = set()
                for i in all:
                    if str(i).__contains__("P166"):
                        for award in i:
                            if award.text != '' and not award.text.__contains__('(') and not award.text.__contains__('»') \
                                    and not award.text.__contains__('«'): awards.add(award.text)
                        return awards
                return list(awards)
            except Exception:
                return list()

    default_url = 'https://ru.wikipedia.org/wiki/'

    def getPerson(self, fname):
        return self.__Person(fname)
