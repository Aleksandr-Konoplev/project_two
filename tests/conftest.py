import os

import pytest

from src.classes_file_operations import folder_data
from src.classes_vacancy import Vacancy, VacancyList


@pytest.fixture
def fake_vacancies():
    """Фейковые данные, которые вернет HH API"""
    return [
        {
            "id": "1",
            "name": "Python Developer",
            "url": "https://hh.ru/vacancy/1",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "requirement": "Опыт Python"
        },
        {
            "id": "2",
            "name": "Data Engineer",
            "url": "https://hh.ru/vacancy/2",
            "salary": {"from": 120000, "to": 180000, "currency": "RUR"},
            "requirement": "Опыт ETL"
        }
    ]


@pytest.fixture
def fixture_response_data():
    """
    Фикстура возвращает фейковые данные API hh.ru для успешного запроса.
    Каждая вакансия теперь имеет дополнительные атрибуты:
    - requirement: описание
    - salary: ожидаемая зарплата
    - vacancy_id: уникальный идентификатор вакансии
    """
    return {
        'items': [
            {
                'name': 'Python Developer',
                'url': 'https://hh.ru/vacancy/1',
                'requirement': 'Опыт работы с Python 3+, Django или Flask',
                'salary': {'from': 100000, 'to': 150000, 'currency': 'RUR'},
                'vacancy_id': '1'
            },
            {
                'name': 'Backend Developer',
                'url': 'https://hh.ru/vacancy/2',
                'requirement': 'Опыт работы с REST API и PostgreSQL',
                'salary': {'from': 120000, 'to': 170000, 'currency': 'RUR'},
                'vacancy_id': '2'
            }
        ]
    }


@pytest.fixture
def fixture_empty_response():
    """Фикстура для проверки случая, когда API вернул пустой список вакансий."""
    return {'items': []}


@pytest.fixture
def fixture_error_response():
    """Фикстура для имитации ошибки на стороне сервера."""
    return {
        'status_code': 500,
        'text': 'Internal Server Error',
        'json': {'error': 'Internal Server Error'}
    }


@pytest.fixture
def fixture_vacancy_data_full():
    """Пример данных вакансии с полным набором полей"""
    return {
        "id": "123",
        "name": "Python Developer",
        "alternate_url": "https://hh.ru/vacancy/123",
        "salary": {"from": 100000, "to": 150000},
        "snippet": {"requirement": "Опыт с Django, Flask"},
    }


@pytest.fixture
def fixture_vacancy_data_partial():
    """Пример данных вакансии с частично заполненной зарплатой"""
    return {
        "id": "456",
        "name": "Junior Developer",
        "alternate_url": "https://hh.ru/vacancy/456",
        "salary": {"from": 80000, "to": None},
        "snippet": {"requirement": "Знание Python"},
    }


@pytest.fixture
def temp_json_file(tmp_path):
    """Временный файл для тестов"""
    file_path = tmp_path / "vacancies_test.json"
    return file_path.name  # только имя файла, как используется в JSONSaver


@pytest.fixture
def sample_vacancy():
    """Фикстура — одна тестовая вакансия"""
    data = {
        "id": "123",
        "name": "Python Developer",
        "alternate_url": "https://hh.ru/vacancy/123",
        "salary": {"from": 100000, "to": 150000},
        "snippet": {"requirement": "Знание Python и Django"}
    }
    return Vacancy(data)


@pytest.fixture
def sample_vacancy_list(sample_vacancy):
    """Фикстура — список вакансий"""
    vlist = VacancyList()
    vlist.add_one_vacancy(sample_vacancy)
    vlist.add_vacancy_manual_method(
        "Data Engineer",
        "https://hh.ru/vacancy/999",
        200000,
        "Опыт работы с ETL"
    )
    return vlist


@pytest.fixture(autouse=True)
def ensure_data_folder_exists():
    """Создает папку data в случае её отсутствия (имитируем как в проекте)."""
    os.makedirs(folder_data, exist_ok=True)
