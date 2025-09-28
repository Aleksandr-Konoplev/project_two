


class Vacancy:
    """ Класс создает объект из словаря полученного в результате API запроса, 1 словарь - 1 вакансия"""
    name: str
    url: str
    salary: int
    requirement: str

    def __init__(self, vacancy_hh: dict):
        """
        Принимает вакансию в виде словаря и инициирует объект с атрибутами
        name: название вакансии
        url: ссылка на вакансию
        salary: зарплата
        requirement: краткое описание
        """
        self.name = vacancy_hh.get('name', 'Нет названия вакансии')
        self.url = vacancy_hh.get('alternate_url', 'Нет ссылки на вакансию')

        if vacancy_hh.get('salary'):
            # Если указаны и нижняя, и верхняя граница — получаем среднее значение
            if vacancy_hh.get('salary').get('from') and vacancy_hh.get('salary').get('to'):
                self.salary = (int(vacancy_hh.get('salary')['from']) + int(vacancy_hh.get('salary')['to'])) // 2
            # Если указанна только верхняя используем ее
            elif vacancy_hh.get('salary').get('from'):
                self.salary = int(vacancy_hh.get('salary').get('from'))
            # Если указанна только нижняя используем ее
            elif vacancy_hh.get('salary').get('to'):
                self.salary = int(vacancy_hh.get('salary').get('to'))
            # Иначе 0
            else:
                self.salary = 0
        else:
            # Если ключ "salary" отсутствует — ставим 0
            self.salary = 0

        # Получаем краткое описание вакансии
        self.requirement = vacancy_hh.get("snippet", {}).get("requirement", "Нет данных")

        # Проверяем, что хотя бы название и ссылка есть
        if not self.name or not self.url:
            raise ValueError("Некорректные данные для вакансии: нет названия или ссылки")

    @staticmethod
    def init_vacancy_manual_method(name, url, salary, requirement):
        vacancy_dict = dict()
        vacancy_dict['name'] = name
        vacancy_dict['alternate_url'] = url
        vacancy_dict['salary'] = {"from": salary, "to": None}
        vacancy_dict['snippet'] = {'requirement': requirement}
        return Vacancy(vacancy_dict)

    def __str__(self):
        return (f'Название вакансии: {self.name}; \n'
                f'Ссылка на вакансию: {self.url}; \n'
                f'Зарплата: {self.salary}; \n'
                f'Краткое описание: {self.requirement} \n')

    def __repr__(self):
        return (f'Название вакансии: {self.name}; \n'
                f'Ссылка на вакансию: {self.url}; \n'
                f'Зарплата: {self.salary}; \n'
                f'Краткое описание: {self.requirement} \n')


class VacancyList:
    vacancy_list: list

    def __init__(self):
        self.vacancy_list = []

    # Методы добавления
    def add_one_vacancy(self, vacancy):
        """ Добавляет один элемент в список вакансий """
        if isinstance(vacancy, Vacancy):
            self.vacancy_list.append(vacancy)
        else:
            raise TypeError('Можно добавлять только объекты класса Vacancy')

    def add_several_vacancy(self, added_vacancy_list):
        """ Добавляет несколько элементов в список вакансий """
        if all(isinstance(v, Vacancy) for v in added_vacancy_list):
            self.vacancy_list.extend(added_vacancy_list)
        else:
            raise TypeError('Все элементы должны быть объектами класса Vacancy')

    def add_one_vacancy_from_hh(self, added_vacancy_hh):
        """ Добавляет один элемент в список вакансий из элемента json ответа (response[items][i], где i вакансия) """
        added_vacancy = Vacancy(added_vacancy_hh)
        self.vacancy_list.append(added_vacancy)
        return self.vacancy_list

    def add_several_vacancy_from_hh(self, added_vacancy_list_hh):
        added_vacancy_list = [Vacancy(v) for v in added_vacancy_list_hh]
        self.vacancy_list.extend(added_vacancy_list)
        return self.vacancy_list

    def add_vacancy_manual_method(self, name, url, salary, requirement):
        self.vacancy_list.append(Vacancy.init_vacancy_manual_method(name, url, salary, requirement))

    # Методы сортировки
    def sorted_by_salary(self):
        """ Фильтруем вакансии по зарплате """
        return sorted(self.vacancy_list, key=lambda v: v["salary"])
