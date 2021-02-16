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

    def parse(self) -> dict:
        attributes = [attr for attr in dir(self) if attr != 'parse' and not attr.startswith('__')]
        return {property: getattr(self, property, '') for property in attributes}


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
    def g4_count(self):
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
    def р1_txt(self):
        return {tag.name: tag.text for tag in self.soup.find_all("h1")}



    # получаем текст тегов h2
    @property
    def р2_txt(self):
        return {tag.name: tag.text for tag in self.soup.find_all("h2")}


    # получаем текст тегов h3
    @property
    def р3_txt(self):
        return {tag.name: tag.text for tag in self.soup.find_all("h3")}


    # получаем текст тегов h4
    @property
    def р4_txt(self):
        return {tag.name: tag.text for tag in self.soup.find_all("h4")}

    # получаем текст тегов h5
    @property
    def р5_txt(self):
        return {tag.name: tag.text for tag in self.soup.find_all("h5")}


    # получаем текст тегов h6
    @property
    def р6_txt(self):
        return {tag.name: tag.text for tag in self.soup.find_all("h6")}


    # получаем текст meta title
    @property
    def meta_title(self):
        return self.soup.find("meta", property="og:title").get('content', '')


    # получаем текст meta description
    @property
    def meta_description(self):
        return self.soup.find("meta", property="og:description").get('content', '')


    # Выгружаем теги <iframe> кол-во
    @property
    def tag_iframe_count(self):
        return len(self.soup.find_all("iframe"))


    # получаем все текста тегов alt атрибутов изображения
    @property
    def alt_txt(self):
        return self.soup.find("alt", property="og:description").get('content', '')


    # получаем кол-во символов на странице, все заголовки
    @property
    def count_symbol(self):
        {tag.name: tag.text for tag in self.soup.find_all("p")}


    # выгрузить весь текстов тегов href на сайте
    @property
    def href_txt(self):
        return self.soup.find("href").get('content', '')


    # Проверка есть ли кодировка utf на сайте
    @property
    def is_utf(self) -> bool:
        page_url = self.soup.find_all('meta charset="UTF-8"')
        return True if page_url else False



url = 'https://habr.com/ru/company/jetinfosystems/blog/542658/'

parser = SiteParser(url)
print(parser.parse())