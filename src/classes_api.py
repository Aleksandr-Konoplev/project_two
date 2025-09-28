import requests
from abc import ABC, abstractmethod


class VacancyAPI(ABC):
    """Абстрактный класс для работы с API сервисов вакансий"""

    @abstractmethod
    def get_vacancies(self, query: str, area: int = None, per_page: int = 5) -> list[dict]:
        """
        Метод для получения вакансий по ключевому слову
        :param query: строка поиска (например, "Python")
        :param area: id региона (например, 1 — Москва)
        :param per_page: количество вакансий на странице
        :return: список словарей с вакансиями
        """
        pass


class HeadHunterAPI(VacancyAPI):
    """Класс для работы с HeadHunter API """

    BASE_URL = "https://api.hh.ru/vacancies"

    def get_vacancies(self, query: str, area: int = None, per_page: int = 5) -> list[dict]:
        """ Метод возвращает список словарей с вакансиями и исключат дополнительную """

        params = {
            "text": query,
            "per_page": per_page
        }

        if area:
            params["area"] = area

        response = requests.get(self.BASE_URL, params=params)

        if response.status_code != 200:
            raise ConnectionError(f"Ошибка запроса: {response.status_code}, {response.text}")

        data = response.json()
        return data.get('items')


#
#
#
#
#
#
#
#
#
#
#
#
# class Vacancy:
#     """ Класс создает объект из словаря полученного в результате API запроса """
#
#     def __init__(self, vacancies_list: dict):
#         """
#         Принимает вакансию в виде словаря и инициирует объект с атрибутами
#         :param vacancies_list: одна вакансия в виде словаря
#         name название вакансии
#         url ссылка на вакансию
#         salary зарплата
#         requirement краткое описание
#         """
#         self.name = vacancies_list.get('name', 'Нет названия вакансии')
#         self.url = vacancies_list.get('alternate_url', 'Нет ссылки на вакансию')
#
#         if vacancies_list.get('salary'):
#             # Если указаны и нижняя, и верхняя граница — получаем среднее значение
#             if vacancies_list.get('salary').get('from') and vacancies_list.get('salary').get('to'):
#                 self.salary = (vacancies_list.get('salary')['from'] + vacancies_list.get('salary')['to']) // 2
#             # Если указанна только верхняя используем ее
#             elif vacancies_list.get('salary').get('from'):
#                 self.salary = vacancies_list.get('salary').get('from')
#             # Если указанна только нижняя используем ее
#             elif vacancies_list.get('salary').get('to'):
#                 self.salary = vacancies_list.get('salary').get('to')
#             # Иначе 0
#             else:
#                 self.salary = 0
#         else:
#             # Если ключ "salary" отсутствует — ставим 0
#             self.salary = 0
#
#         # Получаем краткое описание вакансии
#         self.requirement = vacancies_list.get("snippet", {}).get("requirement", "Нет данных")
#
#         # Проверяем, что хотя бы название и ссылка есть
#         if not self.name or not self.url:
#             raise ValueError("Некорректные данные для вакансии: нет названия или ссылки")
#
#     @staticmethod
#     def cast_to_object_list(vacancies_list_api: list):
#         vacancies_list = []
#         for v in vacancies_list_api:
#             name = v.get('name', 'Нет названия вакансии')
#             url = v.get('alternate_url', 'Нет ссылки на вакансию')
#
#             if v.get('salary'):
#                 # Если указаны и нижняя, и верхняя граница — получаем среднее значение
#                 if v.get('salary').get('from') and v.get('salary').get('to'):
#                     salary = (v.get('salary')['from'] + v.get('salary')['to']) // 2
#                 # Если указанна только верхняя используем ее
#                 elif v.get('salary').get('from'):
#                     salary = v.get('salary').get('from')
#                 # Если указанна только нижняя используем ее
#                 elif v.get('salary').get('to'):
#                     salary = v.get('salary').get('to')
#                 # Иначе 0
#                 else:
#                     salary = 0
#             else:
#                 # Если ключ "salary" отсутствует — ставим 0
#                 salary = 0
#
#             # Получаем краткое описание вакансии
#             requirement = v.get("snippet", {}).get("requirement", "Нет данных")
#
#             # Проверяем, что хотя бы название и ссылка есть
#             if not name or not url:
#                 raise ValueError("Некорректные данные для вакансии: нет названия или ссылки")
#
#             vacancies_list.append({'name': name, 'url': url, 'salary': salary, 'requirement': requirement})
#
#         return vacancies_list
#
#
#
#
#
#
#
#     # def __lt__(self, other):
#     #     """self < other"""
#     #     return self.salary < other.salary
#     #
#     # def __le__(self, other):
#     #     """self <= other"""
#     #     return self.salary <= other.salary
#     #
#     # def __eq__(self, other):
#     #     """self == other"""
#     #     return self.salary == other.salary
#     #
#     # def __gt__(self, other):
#     #     """self > other"""
#     #     return self.salary > other.salary
#     #
#     # def __ge__(self, other):
#     #     """self >= other"""
#     #     return self.salary >= other.salary
#
#
# class Vacancies:
#     vacancies_list = list
#
#     def __init__(self, vacancies_list):
#         self.vacancies_list = vacancies_list
#
#     def sorted_by_salary(self):
#         """ Фильтруем вакансии по зарплате """
#         return sorted(self.vacancies_list, key=lambda v: v["salary"])
