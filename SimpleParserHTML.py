from urllib.request import urlopen, Request  # для открытия, чтения и запроса URL-адреса
from urllib.error import HTTPError, URLError  # импорт ошибок
from html.parser import HTMLParser  # парсинг данных из HTML-кода
import re  # регулярные выражения


class Scraper(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = {}  # словарь с тегами
        self.counter = 0  # счётчик для тегов словаря
        self.tags = []  # список для перечня тегов
        self.tag_bool = False  # переменная отслеживающая открытость тегов

    def handle_starttag(self, tag, attrs):
        self.tag_bool = True
        self.tags.append(tag)
        # сохраняем номер строки и тег в качестве ключа, а аттрибуты в качестве значений (список пар кортежей)
        self.data[(self.counter, tag)] = attrs
        self.counter += 1  # увеличиваем счётчик на 1

    def handle_data(self, data):
        # если в html документе первая строка пустая, то в первую очередь сработает эта функция
        # поэтому получение данных из тегов мы начинаем только если был получен хотя бы один открытый тег
        if self.tag_bool:
            *_, last = self.data.keys()  # ...получаем последний элемент из словаря
            self.data[last].append(data)  # ...и записываем в него текст из тега


class SimpleParser:
    def __init__(self, url, headers, save="", file=""):
        self.url = url
        self.headers = headers
        self.data = None

        if file != "":  # если указан файл для парсинга, ТО
            with open(file, "r", encoding="utf-8") as HTMLtext:  # сохраняем данные из файла в переменную для парсинга
                html = HTMLtext.read()
        else:  # если файл не указан, то парсим данные напрямую с сайта
            try:
                request = Request(url, headers=headers)  # запрос страницы
                response = urlopen(request).read()  # читаем страницу
            except HTTPError as e:
                print(f"Ошибка HTTP: {e.code}")
            except URLError as e:
                print(f"Ошибка URL: {e.reason}")
            else:
                html = response.decode("utf-8")  # декодируем и сохраняем html-код

        if save != "":  # если указано имя файла для сохранения, ТО
            # сохраняем не обработанный html-код в файл
            with open(save, "w", encoding="utf-8") as HTMLtext:
                HTMLtext.write(html)

        self.data = self.__analysis_html(html)  # сохраняем отобранные данные в переменной

    def __analysis_html(self, html):
        html = self.__clear_html(html)  # очищаем текст html
        parser = Scraper()
        parser.feed(html)  # запускаем парсинг

        return parser.data

    def __clear_html(self, html):  # очищаем код html
        html = html.replace("\n", " ")  # заменяем переводы строк на пробелы
        html = re.sub("<br(.*?)>", "", html)  # убираем разделители
        html = re.sub("<script(.*?)</script>", "", html)  # убираем теги со скриптами
        html = re.sub("<svg(.*?)</svg>", "", html)  # убираем теги с векторной графикой
        html = re.sub("<style(.*?)</style>", "", html)  # убираем теги со стилями

        return html

    def get_text(self, request):  # получить текст из тега
        output = None

        for req in self.data:  # перебираем словарь с данными из html
            match len(request):
                case 1:  # если передано только одна значение - тег
                    if req[1] == request[0]:
                        output = self.data[req][-1]
                        break
                case 2:  # если передано два значения - тег и аттрибут
                    if req[1] == request[0] and request[1] in self.data[req]:
                        output = self.data[req][-1]
                        break
                case 3:  # если передано три значения - тег, аттрибут и аттрибут для извлечения из него текста
                    if req[1] == request[0] and request[1] in self.data[req]:
                        for attr in self.data[req]:  # перебираем список с аттрибутами
                            if attr[0] == request[2]:  # если найден искомый аттрибут, ТО
                                output = attr[1]  # ...получаем значение аттрибута
                                break

        return output

    def get_all_text(self, request):  # получить текст из всех одинаковых тегов
        output = []

        for req in self.data:  # перебираем словарь с данными из html
            match len(request):
                case 1:  # если передано только одна значение - тег
                    if req[1] == request[0]:
                        output.append(self.data[req][-1])
                case 2:  # если передано два значения - тег и аттрибут
                    if req[1] == request[0] and request[1] in self.data[req]:
                        output.append(self.data[req][-1])
                case 3:  # если передано три значения - тег, аттрибут и аттрибут для извлечения из него текста
                    if req[1] == request[0] and request[1] in self.data[req]:
                        for attr in self.data[req]:  # перебираем список с аттрибутами
                            if attr[0] == request[2]:  # если найден искомый аттрибут, ТО
                                output.append(attr[1])  # ...получаем значение аттрибута

        return output

