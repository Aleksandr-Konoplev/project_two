from unittest.mock import MagicMock, patch

import pytest

from src.classes_api import HeadHunterAPI


def test_get_vacancies_success(fixture_response_data):
    """Проверяем корректную работу метода при успешном ответе API."""
    with patch('src.classes_api.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = fixture_response_data
        mock_get.return_value = mock_response

        api = HeadHunterAPI()
        result = api.get_vacancies('Python', per_page='2')

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]['name'] == 'Python Developer'

        # Проверяем, что был вызван get с нужными параметрами
        mock_get.assert_called_once()
        called_args, called_kwargs = mock_get.call_args
        assert 'params' in called_kwargs
        assert called_kwargs['params'] == {'text': 'Python', 'per_page': 2}


def test_get_vacancies_with_area(fixture_empty_response):
    with patch('src.classes_api.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = fixture_empty_response
        mock_get.return_value = mock_response

        api = HeadHunterAPI()
        api.get_vacancies('Python', area=1, per_page='3')

        mock_get.assert_called_once()
        _, called_kwargs = mock_get.call_args
        assert called_kwargs['params'] == {'text': 'Python', 'per_page': 3, 'area': 1}


def test_get_vacancies_connection_error(fixture_error_response):
    """Проверяем, что выбрасывается ConnectionError при ответе 500."""

    with patch('src.classes_api.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = 'Internal Server Error'
        mock_response.json.return_value = fixture_error_response
        mock_get.return_value = mock_response

        api = HeadHunterAPI()

        with pytest.raises(ConnectionError) as exc_info:
            api.get_vacancies('Python')

        assert 'Ошибка запроса: 500' in str(exc_info.value)
