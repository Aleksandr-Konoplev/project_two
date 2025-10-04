# HeadHunter вакансии
Приложение для получения при помощи API сервиса платформы HeadHunter вакансий и записи их в файл, а также имеет методы их сортировки

## Содержание
- [Модуль classes_vacancy](#Модуль-classes_vacancy)

## Модуль "classes_vacancy"
### Класс Vacancy
Класс Vacancy инициализирует объект вакансии используя данные из json ответа с атрибутами: name, url, salary, requirement. Также имеет метод init_vacancy_manual_method для ручной инициализации объекта передав данные атрибутов в ручном режиме.
#### Атрибуты:
- name: str (название вакансии)  
- url: str (ссылка на вакансию)
- salary: int (зарплата)
- requirement: str (краткое описание вакансии)
### Класс VacancyList
Класс VacancyList инициализирует объект с атрибутом vacancy_list, который является списком объектов класса Vacancy. Класс имеет методы для добавления вакансий и их сортировки
#### Методы:
- add_one_vacancy - Добавляет один элемент класса Vacancy в список vacancy_list
- add_several_vacancy - Добавляет список элементов класса Vacancy в список vacancy_list
- add_one_vacancy_from_hh - Добавляет один элемент в список vacancy_list из json ответа вызывая класс Vacancy
- add_several_vacancy_from_hh - Добавляет список элементов в список vacancy_list из списка json ответов вызывая класс Vacancy в цикле
- add_vacancy_manual_method - Добавляет один элемент в список vacancy_list принимая значения атрибутов от пользователя, используя Vacancy.init_vacancy_manual_method
- sorted_by_salary = Сортирует список вакансий по зарплате

