from abc import ABC, abstractmethod

import requests
from typing import Union


class VacancyAPI(ABC):
    """Абстрактный класс для работы с API сервисов вакансий"""

    def __init__(self, base_url: str, endpoint: str):
        self.__base_url = base_url
        self.__endpoint = endpoint

    @abstractmethod
    def get_vacancies(self, query: str, area: int | None, per_page: str | None,
                      employer_ids: Union[str, list[str], None]) -> list[dict]:
        """
        Метод для получения вакансий по ключевому слову
        :param query: строка поиска
        :param area: id региона
        :param per_page: количество вакансий на странице
        :param employer_ids: Список id работодателей
        :return: список словарей с вакансиями
        """
        pass

    def _request(self, params: dict | None = None) -> dict:
        """Универсальный метод запроса к API."""
        pass


class HeadHunterAPI(VacancyAPI):
    """Класс для работы с HeadHunter API"""

    def __init__(self, base_url: str = 'https://api.hh.ru', endpoint: str = '/vacancies'):
        super().__init__(base_url, endpoint)
        self.__base_url = base_url
        self.__endpoint = endpoint

    def get_vacancies(self, query: str, area: int | None = 113, per_page: str | None = '10',
                      employer_ids: Union[str, list[str], None] = None) -> list[dict]:
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

        if employer_ids:
            params['employer_id'] = employer_ids

        return self.__request_vacancies(params=params)

    def __request_vacancies(self, params):
        """Приватный метод — выполняет запрос к API. Пользователь напрямую его не вызывает."""

        data = self._request(params)
        return data.get('items')

    def _request(self, params: dict | None = None) -> dict:
        """Универсальный метод запроса к API."""

        url = f'{self.__base_url}{self.__endpoint}'
        response = requests.get(url, params=params)

        if response.status_code != 200:
            raise ConnectionError(f'Ошибка запроса: {response.status_code}, {response.text}')

        return response.json()


if __name__ == '__main__':
    import json

    emp_ids = [
        '1740', # Яндекс
        '104628' # Газпром
    ]

    hh_api = HeadHunterAPI()
    res = hh_api.get_vacancies('', employer_ids=emp_ids)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=4)