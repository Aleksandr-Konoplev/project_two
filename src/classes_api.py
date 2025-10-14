from abc import ABC, abstractmethod
import requests


class VacancyAPI(ABC):
    """Абстрактный класс для работы с API сервисов вакансий"""

    def __init__(self, base_url: str, endpoint: str):
        self.__base_url = base_url  # приватный атрибут
        self.__endpoint = endpoint  # приватный атрибут

    @abstractmethod
    def get_vacancies(self, query: str, area: int | None = None, per_page: int = 10) -> list[dict]:
        """
        Метод для получения вакансий по ключевому слову
        :param query: строка поиска
        :param area: id региона
        :param per_page: количество вакансий на странице
        :return: список словарей с вакансиями
        """
        pass

    def _request(self, params: dict | None = None) -> dict:
        """Универсальный метод запроса к API."""

        url = f'{self.__base_url}{self.__endpoint}'
        response = requests.get(url, params=params)

        if response.status_code != 200:
            raise ConnectionError(f'Ошибка запроса: {response.status_code}, {response.text}')

        return response.json()


class HeadHunterAPI(VacancyAPI):
    """Класс для работы с HeadHunter API"""

    def __init__(self):
        super().__init__(base_url='https://api.hh.ru', endpoint='/vacancies')

    def get_vacancies(self, query: str, area: int | None = None, per_page: int = 10) -> list[dict]:
        try:
            per_page = int(per_page)
        except ValueError:
            per_page = 50
        if per_page > 100 or per_page < 1:
            per_page = 100

        params = {
            'text': query,
            'per_page': per_page
        }
        if area:
            params['area'] = area

        return self.__request_vacancies(params=params)

    def __request_vacancies(self, params):
        """Приватный метод — выполняет запрос к API. Пользователь напрямую его не вызывает."""

        data = self._request(params)
        return data.get('items')
