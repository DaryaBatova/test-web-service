## Ресурс Page
### Описание ресурса 
Содержит информацию о странице следующего вида: количество найденных на странице тегов `<h1>`, `<h2>`, `<h3>` и список ссылок из атрибута `href` тега `<a>`. 
### Конечная точка и методы
```
Endpoints

GET page/{id}

Получить информацию по идентификатору страницы.
```

```
Endpoints

POST page/

Создать информацию для новой страницы.
```
### Параметры path
```
GET page/{id}
```
| Параметр URL      | Описание параметра              |
| --------------    | ---------------------------     |
| id             | Идентификатор страницы (целое число)     |

### Параметры тела запроса
```
POST page/
```
```
{
    "url": "some_url",
}
```
| Параметр тела запроса      | Описание параметра              |
| --------------    | ---------------------------     |
| url              | URL произвольной страницы (строка)     |

### Пример GET запроса
Пример GET-запроса:
```
[base]/page/1
```
### Пример и схема ответа на GET запрос
В качестве ответа на запрос из примера будет получено:
```
{
    "a": [
        "#requests-http-for-humans",
        "https://requests.readthedocs.io/",
        "https://fr.python-requests.org/",
        "https://de.python-requests.org/",
        "https://jp.python-requests.org/",
        "https://cn.python-requests.org/",
        "https://pt.python-requests.org/",
        "https://it.python-requests.org/",
        "https://es.python-requests.org/",
        "https://kenreitz.org/projects",
        "https://github.com/requests/requests"
    ],
    "h1": 1,
    "h2": 5,
    "h3": 3,
    "page_id": 11
}
```

Параметры ответа:

| №   | Параметр    | Тип      | Описание                         |
| --- | ----------- | -------- | -------------------------------- |
|1.   | page_id     | id       | Идентификатор страницы        |
|2.   | h1          | integer   | Количество тегов h1 на странице        |
|3.   | h1          | integer   | Количество тегов h2 на странице |
|4.   | h1          | integer   | Количество тегов h3 на странице             |
|5.   | a           |  array of strings  | Список ссылок на странице |


### Примеры и схемы ответа на POST запрос
* Не передали параметры:
```
http --json POST http://127.0.0.1:8000/page/
```
Схема ответа:
```
{
    "detail": "Invalid parameters: {}. Expected: {'url': 'some_url'}"
}
```

* Передали правильные параметры, но имеются проблемы с запросом страницы по переданному URL в теле запроса:
```
http --json POST http://127.0.0.1:8000/page/ url="http://"
```
Схема ответа:
```
{
    "detail": "An error occurred while trying to establish a connection with http://"
}
```
* Правильно сформировали запрос:
```
http --json POST http://127.0.0.1:8000/page/ url="http://google.com"
```
Схема ответа совпадет со схемой ответа при GET запросе.