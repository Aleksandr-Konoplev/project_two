class Vacancy:
    """ Класс создает объект из словаря полученного в результате API запроса, 1 словарь - 1 вакансия,
    или введя данные о вакансии в ручном режиме используя метод 'init_vacancy_manual_method' """
    __slots__ = ("__vacancy_id", "__name", "__url", "__salary", "__requirement")

    def __init__(self, vacancy_hh: dict):
        """
        Принимает вакансию в виде словаря и инициирует объект с атрибутами
        __vacancy_id: ID вакансии
        __name: название вакансии
        __url: ссылка на вакансию
        __salary: зарплата
        __requirement: краткое описание
        """
        self.__vacancy_id = vacancy_hh.get('id', 'id отсутствует')
        self.__name = vacancy_hh.get('name', 'Нет названия вакансии')
        self.__url = vacancy_hh.get('alternate_url', 'Нет ссылки на вакансию')
        self.__salary = self.__parse_salary(vacancy_hh.get('salary'))  # обрабатываем структуру зарплаты
        self.__requirement = vacancy_hh.get('snippet', {}).get('requirement', 'Нет данных')

    @staticmethod
    def __parse_salary(salary_dict):
        """
        Приватный метод. Принимает словарь salary, который может иметь разную структуру.
        Возвращает целое число — итоговую зарплату.
        """
        if not salary_dict:
            return 0
        # Если указаны обе границы — берём среднее значение
        if salary_dict.get('from') and salary_dict.get('to'):
            return (int(salary_dict['from']) + int(salary_dict['to'])) // 2
        # Если указана только нижняя граница
        if salary_dict.get('from'):
            return int(salary_dict['from'])
        # Если указана только верхняя граница
        if salary_dict.get('to'):
            return int(salary_dict['to'])
        # Если данных нет — считаем зарплату равной 0
        return 0

    @staticmethod
    def init_vacancy_manual_method(name, url, salary, requirement, vacancy_id='Создана в ручную'):
        """ Метод создания вакансии в ручную """
        vacancy_dict = dict()
        vacancy_dict['id'] = vacancy_id
        vacancy_dict['name'] = name
        vacancy_dict['alternate_url'] = url
        vacancy_dict['salary'] = {'from': salary, 'to': None}
        vacancy_dict['snippet'] = {'requirement': requirement}
        return Vacancy(vacancy_dict)

    def __str__(self):
        return (f'\nНазвание вакансии: {self.__name}; \n'
                f'Ссылка на вакансию: {self.__url}; \n'
                f'Зарплата: {self.__salary}; \n'
                f'Краткое описание: {self.__requirement} \n')

    def __repr__(self):
        return (f'\nНазвание вакансии: {self.__name}; \n'
                f'Ссылка на вакансию: {self.__url}; \n'
                f'Зарплата: {self.__salary}; \n'
                f'Краткое описание: {self.__requirement} \n')

    # ID
    @property
    def vacancy_id(self):
        """Возвращает ID вакансии (только чтение)."""
        return self.__vacancy_id

    # Название вакансии
    @property
    def name(self):
        """Возвращает название вакансии (только для чтения)."""
        return self.__name

    # Ссылка
    @property
    def url(self):
        """Возвращает ссылку на вакансию (только чтение)."""
        return self.__url

    # Зарплата
    @property
    def salary(self):
        """Возвращает зарплату вакансии"""
        return self.__salary

    @salary.setter
    def salary(self, new_value_salary):
        """
        Позволяет изменить зарплату, но с проверкой корректности.
        Нельзя установить отрицательную зарплату или нечисловое значение.
        """
        if not isinstance(new_value_salary, (int, float)) or new_value_salary < 0:
            raise ValueError('Зарплата должна быть положительным числом')
        self.__salary = int(new_value_salary)

    # Описание
    @property
    def requirement(self):
        """Краткое описание вакансии (можно изменять)."""
        return self.__requirement

    @requirement.setter
    def requirement(self, new_requirement):
        """Изменение описания."""
        if not isinstance(new_requirement, str):
            raise TypeError('Описание должно быть строкой')
        self.__requirement = new_requirement


class VacancyList:
    vacancy_list: list

    def __init__(self):
        self.vacancy_list = []

    def __iter__(self):
        return iter(self.vacancy_list)

    # Методы добавления
    def add_one_vacancy(self, vacancy):
        """ Добавляет один элемент класса Vacancy в список вакансий """
        if isinstance(vacancy, Vacancy):
            self.vacancy_list.append(vacancy)
            return self
        else:
            raise TypeError('Можно добавлять только объекты класса Vacancy')

    def add_several_vacancy(self, added_vacancy_list):
        """ Добавляет несколько элементов класса Vacancy в список вакансий """
        if all(isinstance(vacancy, Vacancy) for vacancy in added_vacancy_list):
            self.vacancy_list.extend(added_vacancy_list)
            return self
        else:
            raise TypeError('Все элементы должны быть объектами класса Vacancy')

    def add_one_vacancy_from_hh(self, added_vacancy_hh):
        """ Добавляет один элемент в список вакансий из элемента json ответа (response[items][i], где i вакансия) """
        added_vacancy = Vacancy(added_vacancy_hh)
        self.vacancy_list.append(added_vacancy)
        return self

    def add_several_vacancy_from_hh(self, added_vacancy_list_hh):
        """ Добавляет несколько элементов в список вакансий из json ответа (response[items][i], где i вакансия) """
        added_vacancy_list = [Vacancy(v) for v in added_vacancy_list_hh]
        self.vacancy_list.extend(added_vacancy_list)
        return self

    def add_vacancy_manual_method(self, name, url, salary, requirement, vacancy_id='Добавлена в ручную'):
        """Добавляет один элемент в ручном режиме"""
        self.vacancy_list.append(Vacancy.init_vacancy_manual_method(name, url, salary, requirement, vacancy_id))
        return self

    # Методы сортировки и фильтрации
    def sorted_by_salary(self, reverse_sort: bool = True):
        """ Сортируем вакансии по зарплате """
        self.vacancy_list = sorted(self.vacancy_list, key=lambda v: v.salary, reverse=reverse_sort)
        return self

    def filter_by_salary(self, salary_range):
        """ Фильтруем вакансии по диапазону зарплаты, если передана одна ЗП отбирает вакансии не ниже этой ЗП """
        if salary_range in ('', ' '):
            print('Введен не корректный диапазон зарплат, установлена зп в размере 1')
            salary_rl = [1]
        else:
            salary_rl = [int(i) for i in salary_range.split('-')]
        # Проверяем что все элементы принадлежат типу int и их не более 2
        if not all(isinstance(x, int) for x in salary_rl) or not len(salary_rl) in (1, 2):
            print('Введен не корректный диапазон зарплат, установлена зп в размере 1')
            salary_rl = [1]
        if len(salary_rl) == 1:
            self.vacancy_list = list(filter(lambda v: salary_rl[0] <= v.salary, self.vacancy_list))
            return self
        else:
            self.vacancy_list = list(filter(lambda v: salary_rl[0] <= v.salary <= salary_rl[1], self.vacancy_list))
            return self

    def filter_by_req(self, filter_words):
        """Фильтрация вакансий по ключевым словам в requirement"""
        if filter_words in ([], None):
            return self
        self.vacancy_list = list(
            filter(
                lambda v: v.requirement and any(word.lower() in v.requirement.lower() for word in filter_words),
                self.vacancy_list
            )
        )
        return self

    def get_top_vacancies(self, top_n):
        """Отбрасывает все вакансии кроме первых top_n"""
        if not isinstance(top_n, int) or top_n < 1:
            top_n = 1
        self.vacancy_list = self.vacancy_list[0: top_n]
        return self
