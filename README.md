# HeadHunter Vacancy Management System

Комплексная система для сбора, анализа и управления вакансиями с платформы HeadHunter с использованием PostgreSQL и REST API.

## Описание проекта

Это полнофункциональное Python-приложение для автоматизации работы с вакансиями на платформе hh.ru. Система интегрируется с публичным API HeadHunter, сохраняет данные в PostgreSQL базу данных и предоставляет мощные инструменты для анализа рынка труда.

## Основные возможности

- 🔍 **Поиск вакансий** через API HeadHunter по ключевым словам и работодателям
- 🏢 **Получение данных о компаниях** с информацией о работодателях
- 🗄️ **PostgreSQL интеграция** для надежного хранения и быстрого поиска
- 💰 **Аналитика по зарплатам** с расчетом средних значений и фильтрацией
- 📊 **SQL-запросы** для статистического анализа данных
- 💾 **Экспорт в JSON** для дальнейшей работы с данными
- ➕ **Управление данными**: добавление, обновление, удаление вакансий
- 🎯 **Фильтрация и сортировка** по множеству критериев
- ✅ **Полное покрытие тестами** с использованием pytest

## Структура проекта

```
project_two/
├── src/                              # Исходный код приложения
│   ├── __init__.py                   # Инициализация пакета
│   ├── classes_vacancy.py            # Классы Vacancy и VacancyList
│   ├── classes_api.py                # API клиент для HeadHunter
│   ├── classes_file_operations.py    # JSON операции с файлами
│   ├── db_connect.py                 # Управление PostgreSQL базой данных
│   └── config.py                     # Парсер конфигурационных файлов
├── tests/                            # Модульные тесты (pytest)
├── htmlcov/                          # HTML отчеты о покрытии кода
├── main.py                           # Точка входа в приложение
├── pyproject.toml                    # Конфигурация Poetry и зависимости
├── poetry.lock                       # Файл блокировки версий зависимостей
├── .flake8                           # Конфигурация линтера
├── database.ini                      # Параметры подключения к PostgreSQL
└── README.md                         # Документация проекта
```

## Основные компоненты

### 1. Классы вакансий (`classes_vacancy.py`)

#### Класс `Vacancy`
Представляет отдельную вакансию с инкапсулированными приватными атрибутами:

**Приватные атрибуты:**
- `__vacancy_id`: Уникальный идентификатор вакансии
- `__name`: Название должности
- `__url`: Ссылка на объявление
- `__salary`: Зарплата (среднее значение из диапазона)
- `__requirement`: Краткое описание требований

**Ключевые методы:**
- `__init__(vacancy_dict)`: Инициализация из словаря API с валидацией данных
- `__parse_salary()`: Парсинг диапазона зарплаты в единое числовое значение
- `init_vacancy_manual_method()`: Статический метод для ручного создания вакансии
- Property-методы с геттерами для всех атрибутов
- Сеттеры для `salary` и `requirement` с валидацией типов

**Валидация данных:**
- ID должен быть строкой или числом
- Название, URL и требования должны быть строками
- Зарплата должна быть неотрицательным числом

#### Класс `VacancyList`
Управляет коллекцией объектов `Vacancy` с поддержкой цепочки вызовов:

**Методы добавления:**
- `add_one_vacancy(vacancy)`: Добавление одного объекта `Vacancy`
- `add_several_vacancy(vacancies)`: Добавление списка объектов
- `add_one_vacancy_from_hh(vacancy_dict)`: Создание вакансии из словаря API
- `add_several_vacancy_from_hh(vacancy_dicts)`: Создание нескольких вакансий из API
- `add_vacancy_manual_method(params)`: Ручное добавление с параметрами

**Методы фильтрации и сортировки:**
- `sorted_by_salary(ascending=True)`: Сортировка по зарплате (возрастание/убывание)
- `filter_by_salary(salary_range)`: Фильтрация по диапазону (например, "50000-100000")
- `filter_by_req(keywords)`: Поиск по ключевым словам в описании
- `get_top_vacancies(top_n)`: Получение топ-N вакансий

**Дополнительно:**
- Реализует `__iter__` для итерации по списку
- Поддерживает method chaining (цепочку методов)

### 2. API интеграция (`classes_api.py`)

#### Абстрактный класс `VacancyAPI`
Определяет базовый интерфейс для работы с API вакансий:
- `get_vacancies()`: Абстрактный метод для получения вакансий
- `_request()`: Базовый метод для HTTP запросов

#### Класс `HeadHunterAPI`
Конкретная реализация для работы с API hh.ru:

**Методы:**
- `get_vacancies(search_query, area=113, per_page=100, employer=None)`:
  - `search_query`: Ключевые слова для поиска
  - `area`: Код региона (по умолчанию 113 - Россия)
  - `per_page`: Количество результатов на странице (1-100)
  - `employer`: ID работодателя для фильтрации (опционально)

- `get_employer_by_id(employer_id)`: Получение данных о работодателе
  - Возвращает название компании и URL профиля

- `__request_vacancies()`: Приватный метод для запросов вакансий
- `_request()`: Универсальный HTTP GET с обработкой ошибок

**Особенности:**
- Валидация параметра `per_page` (конвертация в int, проверка диапазона 1-100)
- Парсинг JSON ответов с проверкой ошибок
- Обработка HTTP статус-кодов (исключение при != 200)

### 3. Работа с файлами (`classes_file_operations.py`)

#### Абстрактный класс `ConnectFile`
Базовый интерфейс для файловых операций:
- `save_vacancies_to_file()`: Сохранение коллекции вакансий
- `add_vacancy_to_file()`: Добавление одной вакансии
- `add_vacancy_list_to_file()`: Добавление списка вакансий
- `del_vacancy_from_file()`: Удаление по URL
- `search_vacancy()`: Поиск вакансий в файле

#### Класс `JSONSaver`
Реализация для работы с JSON файлами:

**Конструктор:**
- `__init__(filename='vacancy.json')`: Инициализация с именем файла

**Основные методы:**
- `save_vacancies_to_file(vacancy_list)`: Конвертация `VacancyList` в JSON
  - Структура: id, name, url, salary, requirement
  - UTF-8 кодировка, отступы 4 пробела

- `add_vacancy_to_file(vacancy)` / `add_vacancy_list_to_file(vacancies)`:
  - Проверка существования файла
  - Чтение текущих данных
  - Добавление новых записей
  - Перезапись с обновленными данными

- `del_vacancy_from_file(url)`:
  - Поиск по URL (поддержка вакансий без ID)
  - Обратная связь об успехе/неудаче операции

- `get_file_path()`: Получение полного пути к файлу

### 4. Работа с базой данных (`db_connect.py`)

#### Абстрактный класс `AbstractDBM`
Определяет интерфейс для управления базой данных:
- `create_db()`, `update_db()`, `delete_db()`, `read_db()`

#### Класс `DBManager`
Полнофункциональный менеджер PostgreSQL базы данных:

**Инициализация:**
- `__init__(params, db_name=None)`: Подключение к PostgreSQL через psycopg2
- Создание connection и cursor объектов

**Операции с базой данных:**
- `create_db()`: Создание БД и таблиц (employers, vacancies)
  - Схема таблицы employers: id, name, url
  - Схема таблицы vacancies: id, employer_id, name, url, salary, requirement

- `update_db(employers, vacancies)`: Массовая вставка/обновление данных
  - Использует UPSERT логику (ON CONFLICT)
  - Параметризованные запросы для защиты от SQL-инъекций

- `delete_db()`: Удаление базы данных
  - Завершение активных подключений
  - Полное удаление БД

**Методы запросов:**
- `get_companies_and_vacancies_count()`: Компании и количество их вакансий
- `get_all_vacancies()`: Все вакансии с названием компании, зарплатой и URL
- `get_avg_salary()`: Средняя зарплата по всем вакансиям
- `get_vacancies_with_higher_salary()`: Вакансии с зарплатой выше среднего
- `get_vacancies_with_keyword(keyword)`: Поиск по ключевому слову (case-insensitive)

**Безопасность и надежность:**
- Параметризованные SQL запросы
- Транзакции с rollback при ошибках
- Корректная обработка NULL значений в зарплатах
- Подробное логирование в консоль

### 5. Конфигурация (`config.py`)

**Функция `config(filename, section='postgresql')`:**
- Парсинг INI конфигурационных файлов
- Использует `ConfigParser` из стандартной библиотеки
- Кодировка: cp1251
- Возвращает словарь параметров подключения
- Обработка отсутствующих секций (исключение)

### 6. Главный модуль (`main.py`)

**Функция `main()`:**
Основной рабочий процесс приложения:
1. Получение данных о 10 крупных российских компаниях:
   - Yandex, Газпром, Аэрофлот, VK, Сбербанк, Тинькофф и др.
2. Загрузка вакансий через API для каждой компании
3. Создание и наполнение PostgreSQL базы данных
4. Выполнение аналитических SQL-запросов:
   - Расчет средних зарплат
   - Фильтрация по зарплатным порогам
   - Поиск по ключевым словам
   - Вывод списков с названиями компаний
   - Подсчет вакансий по работодателям

**Функция `user_interaction()` (закомментирована):**
Альтернативный интерактивный режим работы:
- Ввод поискового запроса от пользователя
- Фильтрация по ключевым словам и диапазону зарплат
- Опциональная сортировка по зарплате
- Экспорт результатов в JSON файл

## Технологический стек

- **Язык программирования**: Python 3.x
- **База данных**: PostgreSQL
- **Библиотека БД**: psycopg2 (PostgreSQL адаптер)
- **Управление зависимостями**: Poetry
- **HTTP клиент**: requests
- **Тестирование**: pytest (с использованием mock и pytest-cov)
- **Качество кода**: flake8
- **Форматы данных**: JSON, INI
- **Парсинг конфигураций**: ConfigParser

## Установка и настройка

### Требования

- Python 3.8 или выше
- PostgreSQL 12 или выше
- Poetry (для управления зависимостями)

### Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Aleksandr-Konoplev/project_two.git
cd project_two
git checkout feature
```

2. Установите зависимости с помощью Poetry:
```bash
poetry install
```

3. Активируйте виртуальное окружение:
```bash
poetry shell
```

4. Настройте PostgreSQL:
   - Убедитесь, что PostgreSQL запущен
   - Создайте файл `database.ini` в корне проекта:

```ini
[postgresql]
host=localhost
user=your_username
password=your_password
port=5432
```

**Важно**: Замените `your_username` и `your_password` на ваши учетные данные PostgreSQL.

## Использование

### Запуск основного приложения

```bash
python main.py
```

Приложение выполнит следующие действия:

1. Получит данные о 10 крупных российских компаниях через API HeadHunter
2. Загрузит все вакансии этих компаний
3. Создаст PostgreSQL базу данных `hh_vacancies`
4. Заполнит таблицы `employers` и `vacancies`
5. Выполнит серию аналитических запросов:
   - Список компаний с количеством вакансий
   - Все вакансии с деталями (компания, зарплата, ссылка)
   - Средняя зарплата по всем вакансиям
   - Вакансии с зарплатой выше средней
   - Поиск вакансий по ключевому слову

### Режимы работы

#### 1. Режим работы с базой данных (активный)
Автоматический сбор и анализ данных о вакансиях крупных компаний с сохранением в PostgreSQL.

#### 2. Интерактивный режим (закомментирован)
Для использования интерактивного режима раскомментируйте функцию `user_interaction()` в `main.py`:

```python
if __name__ == '__main__':
    user_interaction()
```

Интерактивный режим позволяет:
- Вводить собственные поисковые запросы
- Фильтровать по зарплате и ключевым словам
- Сортировать результаты
- Экспортировать в JSON

## Тестирование

Проект включает комплексный набор модульных тестов, покрывающих:

- Обработку API запросов и ошибок
- Операции с JSON файлами и граничные случаи
- Инициализацию объектов вакансий
- Манипуляции со списками вакансий
- Сортировку по зарплате

### Запуск тестов

```bash
# Запуск всех тестов
pytest

# Запуск с отчетом о покрытии
pytest --cov

# Генерация HTML отчета о покрытии
pytest --cov --cov-report=html
```

## Проверка качества кода

Проект использует flake8 для соблюдения стандартов кодирования:

```bash
flake8
```

## Примеры использования

### 1. Работа с API HeadHunter

```python
from src.classes_api import HeadHunterAPI

# Создание клиента API
api = HeadHunterAPI()

# Поиск вакансий по ключевым словам
vacancies = api.get_vacancies("Python developer", area=113, per_page=50)

# Получение вакансий конкретного работодателя
yandex_vacancies = api.get_vacancies("developer", employer="1740")

# Получение информации о работодателе
employer_info = api.get_employer_by_id("1740")  # Яндекс
print(employer_info)  # [{'name': 'Яндекс', 'url': 'https://hh.ru/employer/1740'}]
```

### 2. Работа с классами вакансий

```python
from src.classes_vacancy import Vacancy, VacancyList

# Создание вакансии из словаря API
vacancy = Vacancy(vacancy_dict_from_api)

# Ручное создание вакансии
manual_vacancy = Vacancy.init_vacancy_manual_method(
    vacancy_id="123",
    name="Senior Python Developer",
    url="https://hh.ru/vacancy/123",
    salary=150000,
    requirement="Python, Django, PostgreSQL"
)

# Работа со списком вакансий
vlist = VacancyList()

# Добавление вакансий разными способами
vlist.add_one_vacancy(vacancy)
vlist.add_several_vacancy_from_hh(vacancies_from_api)
vlist.add_vacancy_manual_method("456", "DevOps Engineer", "url", 120000, "Docker, K8s")

# Цепочка операций (method chaining)
filtered_sorted = (vlist
                   .filter_by_req("Python")
                   .filter_by_salary("100000-200000")
                   .sorted_by_salary(ascending=False)
                   .get_top_vacancies(10))
```

### 3. Сохранение в JSON

```python
from src.classes_file_operations import JSONSaver

# Создание сохранителя
saver = JSONSaver("my_vacancies.json")

# Сохранение списка вакансий
saver.save_vacancies_to_file(vlist)

# Добавление новых вакансий к существующему файлу
saver.add_vacancy_to_file(new_vacancy)
saver.add_vacancy_list_to_file([vacancy1, vacancy2])

# Удаление вакансии по URL
saver.del_vacancy_from_file("https://hh.ru/vacancy/123")

# Получение пути к файлу
print(saver.get_file_path())
```

### 4. Работа с базой данных PostgreSQL

```python
from src.db_connect import DBManager
from src.config import config

# Загрузка конфигурации
db_params = config('database.ini')

# Создание менеджера БД
db = DBManager(db_params, db_name='hh_vacancies')

# Создание базы и таблиц
db.create_db()

# Наполнение базы данными
employers_data = [
    {'id': '1740', 'name': 'Яндекс', 'url': 'https://hh.ru/employer/1740'}
]
vacancies_data = [
    {'id': '12345', 'employer_id': '1740', 'name': 'Python Developer',
     'url': 'https://hh.ru/vacancy/12345', 'salary': 150000,
     'requirement': 'Python, Django'}
]
db.update_db(employers_data, vacancies_data)

# Выполнение запросов
companies = db.get_companies_and_vacancies_count()
all_vacs = db.get_all_vacancies()
avg_salary = db.get_avg_salary()
high_salary_vacs = db.get_vacancies_with_higher_salary()
python_vacs = db.get_vacancies_with_keyword('Python')

# Вывод результатов
for company in companies:
    print(f"{company[0]}: {company[1]} вакансий")

print(f"Средняя зарплата: {avg_salary} руб.")
```

### 5. Полный пример: Анализ рынка труда

```python
from src.classes_api import HeadHunterAPI
from src.classes_vacancy import VacancyList
from src.db_connect import DBManager
from src.config import config

# 1. Получение данных через API
api = HeadHunterAPI()
employers_ids = ["1740", "78638"]  # Яндекс, Сбербанк

employers = []
all_vacancies = []

for emp_id in employers_ids:
    # Получение информации о компании
    employer = api.get_employer_by_id(emp_id)
    employers.extend(employer)

    # Получение вакансий компании
    vacancies = api.get_vacancies("developer", employer=emp_id, per_page=100)
    all_vacancies.extend(vacancies)

# 2. Обработка данных
vlist = VacancyList()
vlist.add_several_vacancy_from_hh(all_vacancies)

# Фильтрация и анализ
high_salary = vlist.filter_by_salary("150000-").sorted_by_salary(ascending=False)
python_jobs = vlist.filter_by_req("Python")

# 3. Сохранение в БД
db_params = config('database.ini')
db = DBManager(db_params, 'market_analysis')
db.create_db()
db.update_db(employers, all_vacancies)

# 4. Аналитика
print(f"Всего вакансий: {len(list(vlist))}")
print(f"С зарплатой >150k: {len(list(high_salary))}")
print(f"Python вакансий: {len(list(python_jobs))}")
print(f"Средняя зарплата: {db.get_avg_salary()}")
```

## Схема базы данных

```sql
-- Таблица работодателей
CREATE TABLE employers (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    url TEXT
);

-- Таблица вакансий
CREATE TABLE vacancies (
    id VARCHAR(255) PRIMARY KEY,
    employer_id VARCHAR(255) REFERENCES employers(id),
    name VARCHAR(255) NOT NULL,
    url TEXT,
    salary INTEGER,
    requirement TEXT
);
```

## Архитектурные особенности

### Паттерны проектирования

1. **Abstract Base Class (ABC)** - используется для:
   - `VacancyAPI` и `HeadHunterAPI`
   - `ConnectFile` и `JSONSaver`
   - `AbstractDBM` и `DBManager`

2. **Builder Pattern** - множественные методы добавления в `VacancyList`:
   - `add_one_vacancy()`, `add_several_vacancy()`
   - `add_one_vacancy_from_hh()`, `add_several_vacancy_from_hh()`
   - `add_vacancy_manual_method()`

3. **Method Chaining** - поддержка цепочки вызовов в `VacancyList`:
   ```python
   vlist.filter_by_req("Python").filter_by_salary("100000-").sorted_by_salary()
   ```

4. **Factory Method** - статический метод `init_vacancy_manual_method()` в классе `Vacancy`

### Принципы SOLID

- **Single Responsibility**: Каждый класс отвечает за одну функциональность
- **Open/Closed**: Расширение через наследование (Abstract классы)
- **Liskov Substitution**: Подклассы могут заменять базовые классы
- **Interface Segregation**: Специфичные интерфейсы для каждой операции
- **Dependency Inversion**: Зависимость от абстракций, а не реализаций

### Безопасность

- Параметризованные SQL запросы (защита от SQL-инъекций)
- Валидация входных данных в конструкторах классов
- Обработка исключений и ошибок HTTP
- Конфигурация БД вынесена в отдельный файл (не в коде)

## Возможные расширения

- ✨ Добавление других платформ поиска работы (SuperJob, Zarplata.ru)
- 📈 Визуализация данных (графики зарплат, трендов)
- 🔔 Система уведомлений о новых вакансиях
- 🤖 ML-модели для рекомендации вакансий
- 🌐 Web-интерфейс на Flask/Django
- 📊 Экспорт в Excel/CSV форматы
- 🔍 Полнотекстовый поиск в PostgreSQL
- 🕐 Scheduled задачи для автоматического обновления

## Часто задаваемые вопросы (FAQ)

### Как изменить список компаний для анализа?

Отредактируйте список `employers_ids` в функции `main()` в файле `main.py`:

```python
employers_ids = ["1740", "78638", "your_company_id"]
```

ID компаний можно найти на hh.ru в URL профиля работодателя.

### Как работать с разными регионами?

Параметр `area` в методе `get_vacancies()`:
- 113 - Россия
- 1 - Москва
- 2 - Санкт-Петербург

Полный список кодов регионов доступен в [API документации HeadHunter](https://api.hh.ru/areas).

### Как увеличить количество получаемых вакансий?

API HeadHunter возвращает максимум 100 вакансий за один запрос. Для получения большего количества:
1. Используйте параметр `page` для пагинации
2. Комбинируйте разные поисковые запросы
3. Фильтруйте по конкретным работодателям

### Почему некоторые вакансии без зарплаты?

Многие работодатели не указывают зарплату в публичных объявлениях. В таких случаях:
- Поле `salary` в БД будет NULL
- Методы фильтрации по зарплате пропускают такие вакансии
- Расчет средней зарплаты исключает NULL значения

## Лицензия

Проект разработан в образовательных целях.

## Автор

**Aleksandr Konoplev**

## Ссылки

- [Репозиторий на GitHub](https://github.com/Aleksandr-Konoplev/project_two)
- [Ветка feature](https://github.com/Aleksandr-Konoplev/project_two/tree/feature)
- [API HeadHunter - Документация](https://api.hh.ru/)
- [API HeadHunter - Вакансии](https://github.com/hhru/api/blob/master/docs/vacancies.md)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Poetry Documentation](https://python-poetry.org/docs/)

---

**Последнее обновление**: 2025-11-09
