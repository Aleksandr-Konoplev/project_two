import pytest
from unittest.mock import patch, MagicMock
from src.classes_api import HeadHunterAPI


def test_get_vacancies_success(fake_response_data):
    """Проверяем корректную работу метода при успешном ответе API."""

    with patch('src.classes_api.requests.get') as mock_get:
        # Настраиваем фейковый ответ
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = fake_response_data
        mock_get.return_value = mock_response

        api = HeadHunterAPI()
        result = api.get_vacancies('Python', per_page=2)

        # Проверяем, что результат корректен
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]['name'] == 'Python Developer'

        # Проверяем, что был вызван правильный запрос
        mock_get.assert_called_once_with(
            api.BASE_URL,
            params={'text': 'Python', 'per_page': 2}
        )


def test_get_vacancies_with_area(fake_empty_response):
    """Проверяем, что параметр area добавляется в запрос."""

    with patch('src.classes_api.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = fake_empty_response
        mock_get.return_value = mock_response

        api = HeadHunterAPI()
        api.get_vacancies('Python', area=1, per_page=3)

        mock_get.assert_called_once_with(
            api.BASE_URL,
            params={'text': 'Python', 'per_page': 3, 'area': 1}
        )


def test_get_vacancies_connection_error(fake_error_response):
    """Проверяем, что выбрасывается ConnectionError при ответе 500."""

    with patch('src.classes_api.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = 'Internal Server Error'
        mock_response.json.return_value = fake_error_response
        mock_get.return_value = mock_response

        api = HeadHunterAPI()

        with pytest.raises(ConnectionError) as exc_info:
            api.get_vacancies('Python')

        assert 'Ошибка запроса: 500' in str(exc_info.value)
