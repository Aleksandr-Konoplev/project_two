import pytest

@pytest.fixture
def fake_response_data():
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
def fake_empty_response():
    """Фикстура для проверки случая, когда API вернул пустой список вакансий."""
    return {'items': []}


@pytest.fixture
def fake_error_response():
    """Фикстура для имитации ошибки на стороне сервера."""
    return {
        'status_code': 500,
        'text': 'Internal Server Error',
        'json': {'error': 'Internal Server Error'}
    }
