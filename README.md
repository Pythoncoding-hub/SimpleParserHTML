# SimpleParserHTML
Простой парсер сайта на языке Python с использованием только стандартной бибилиотеки.
Данный парсер не обрабатывает java-скрипты и контент генерируемый на стороне клиента с помощью этих скриптов.

### КЛАСС SimpleParser
    При создании объекта Вы можете указать следующие параметры:
            [url]      - (обязательный) ссылка на страницу сайта.
            [headers]  - (обязательный) заголовок для запроса.
            [save]     - в этом не обязательном параметре можно указать имя файла для сохранения не обработанного html-кода.
            [file]     - вы также можете указать файл с html-кодом для парсинга.

### Пример кода для парсинга
    from SimpleParserHTML import SimpleParser

    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/131.0.0.0 Safari/537.36",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
           "Sec-Ch-Ua": '"Chromium";v="131", "Not_A Brand";v="24"',
           "Sec-Ch-Ua-Platform": '"Linux"'}  # заголовок

    location = "moscow"  # местоположение
    url = F"https://world-weather.ru/pogoda/russia/{location}/"  # погода сейчас
    html = SimpleParser(url, headers)  # создаём объект парсера

    # получаем текст из ПЕРВОГО тега "h1"
    loc = html.get_text(["h1"])
    print(loc)

    # получаем текст из ПЕРВОГО тега "div" с аттрибутом "id=weather-now-number"
    temp = html.get_text(["div", ("id", "weather-now-number")])
    print(temp)

    # получаем знаечние аттрибута "title" из ПЕРВОГО тега "span" с аттрибутом "id=weather-now-ico"
    weather = html.get_text(["span", ("id", "weather-now-icon"), "title"])
    print(weather)

    # получаем текст из ВСЕХ тегов "span" с аттрибутом "class=hourly-item-time "
    time = html.get_all_text(["span", ("class", "hourly-item-time ")])
    print(time)

    # получаем знаечние аттрибута "title" из ВСЕХ тегов "span" с аттрибутом "id=weather-now-ico"
    weather2 = html.get_all_text(["span", ("class", "hourly-item-icon tooltip  wi n400"), "title"])
    print(weather2)
