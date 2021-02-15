from tokenize import Comment

from bs4 import BeautifulSoup
import requests as req


class SiteParser(object):
    def __init__(self, site_url):
        self.site_url = site_url
        resp = req.get(site_url)
        if resp.status_code == 200:
            self.soup = BeautifulSoup(resp.text, 'lxml')
        else:
            domain = site_url.split('/')[2]
            raise ConnectionError(f'could not fetch domain {domain} html')


    # Получаем домен сайта +
    @property
    def domain(self):
        return self.site_url.split('/')[2]


    # Получаем все мета подключения на сайте +
    @property
    def meta(self):
        page_url = self.soup.find_all("meta")
        return page_url


    # Кол-во тегов h1 +
    @property
    def h1_count(self):
        return len(self.soup.find_all("h1"))


    # Кол-во тегов h2 +
    @property
    def h2_count(self):
        return len(self.soup.find_all("h2"))


    # Кол-во тегов h3 +
    @property
    def h3_count(self):
        return len(self.soup.find_all("h3"))


    # Кол-во тегов h4
    @property
    def getTegH4Count(self):
        return len(self.soup.find_all("h4"))



    # Кол-во тегов h5
    @property
    def h5_count(self):
        return len(self.soup.find_all("h5"))



    # Кол-во тегов h6
    @property
    def h6_count(self):
        return len(self.soup.find_all("h6"))


    # получаем текст тега h1
    @property
    def getTegH1Txt(self):
        soup = BeautifulSoup(resp.text, 'lxml')
        for tag in soup.find_all("h1"):
            return f"{tag.name} txt- {tag.text}"


    # получаем текст тегов h2
    def getTegH2Txt():
        soup = BeautifulSoup(resp.text, 'lxml')
        for tag in soup.find_all("h2"):
            return("{0} txt- {1}".format(tag.name, tag.text))


    # получаем текст тегов h3
    def getTegH3Txt():
        soup = BeautifulSoup(resp.text, 'lxml')
        for tag in soup.find_all("h3"):
            return("{0} txt- {1}".format(tag.name, tag.text))


    # получаем текст тегов h4
    def getTegH4Txt():
        soup = BeautifulSoup(resp.text, 'lxml')
        for tag in soup.find_all("h4"):
            return("{0} txt- {1}".format(tag.name, tag.text))


    # получаем текст тегов h5
    def getTegH5Txt():
        soup = BeautifulSoup(resp.text, 'lxml')
        for tag in soup.find_all("h5"):
            return("{0} txt- {1}".format(tag.name, tag.text))


    # получаем текст тегов h6
    def getTegH6Txt():
        soup = BeautifulSoup(resp.text, 'lxml')
        for tag in soup.find_all("h6"):
            return("{0} txt- {1}".format(tag.name, tag.text))


    # получаем текст meta title
    def getMetaTitle():
        soup = BeautifulSoup(resp.text, 'lxml')
        for tag in soup.find("meta", property="og:title"):
            title = soup.find("meta", property="og:title")
            return("meta title - " + title["content"] if title else "No meta title given")


    # получаем текст meta description
    def getMetaDescription():
        soup = BeautifulSoup(resp.text, 'lxml')
        title = soup.find("meta", property="og:description")
        return("meta description - " + title["content"] if title else "No meta description given")


    # Выгружаем теги <iframe> кол-во
    def getTagIframeCount():
        soup = BeautifulSoup(resp.text, 'lxml')
        col = 0
        for tag in soup.find_all("iframe"):
            col += 1
        return("iframe кол-во - " + str(col))


    # получаем все текста тегов alt атрибутов изображения
    def getAltTxt():
        soup = BeautifulSoup(resp.text, 'lxml')
        title = soup.find("alt", property="og:description")
        return("alt txt - " + title["content"] if title else "No alt txt given")


    # получаем кол-во символов на странице, все заголовки
    def getCountSymbol():
        soup = BeautifulSoup(resp.text, 'lxml')
        for tag in soup.find_all("p"):
            return("{0} txt- {1}".format(tag.name, tag.text))


    # выгрузить весь текстов тегов href на сайте
    def getHrefTxt():
        soup = BeautifulSoup(resp.text, 'lxml')
        title = soup.find("href")
        return("href txt - " + title["content"] if title else "No href txt given")


    # Проверка есть ли кодировка utf на сайте
    def getUtf():
        soup = BeautifulSoup(resp.text, 'lxml')
        page_url = soup.find_all('meta charset="UTF-8"')
        return page_url if page_url else None


    def parse(self):
        pass