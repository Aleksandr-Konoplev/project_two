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
    """Класс для работы с HeadHunter API"""

    BASE_URL = "https://api.hh.ru/vacancies"

    def get_vacancies(self, query: str, area: int = None, per_page: int = 5) -> list[dict]:
        """Метод возвращает список словарей с вакансиями и исключат дополнительную информацию"""

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
