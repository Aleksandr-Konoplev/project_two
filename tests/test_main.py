from unittest.mock import patch

from main import user_interaction
from src.classes_file_operations import JSONSaver


def test_user_interaction_all_options(fake_vacancies):
    inputs = [
        "python",          # search_query
        "2",               # len_vacancy_api_res
        "Python",          # filter_words
        "50000 - 150000",  # salary_range
        "y",               # flag_sort_salary
        "2",               # top_n_res
        "y",               # flag_save_json_file
        "test_file"        # file_name
    ]

    with patch("builtins.input", side_effect=inputs), \
            patch("builtins.print") as mock_print, \
            patch("src.classes_api.HeadHunterAPI.get_vacancies", return_value=fake_vacancies), \
            patch("main.JSONSaver") as MockSaver:  # <-- важно патчить main.JSONSaver

        mock_instance = MockSaver.return_value
        user_interaction()

        # Проверяем что метод сохранения вызвался
        mock_instance.add_vacancy_list_to_file.assert_called_once()

        # Проверяем, что программа завершила работу
        found = any("Программа успешно завершила свою работу" in str(call) for call in mock_print.call_args_list)
        assert found


def test_user_interaction_no_save(fake_vacancies):
    """Тест user_interaction, когда пользователь не сохраняет файл"""

    inputs = [
        "python",          # search_query
        "2",               # len_vacancy_api_res
        "Python",          # filter_words
        "50000 - 150000",  # salary_range
        "y",               # flag_sort_salary
        "2",               # top_n_res
        "n"                # flag_save_json_file
    ]

    with patch("builtins.input", side_effect=inputs), \
         patch("builtins.print"), \
         patch("src.classes_api.HeadHunterAPI.get_vacancies", return_value=fake_vacancies), \
         patch.object(JSONSaver, "add_vacancy_list_to_file") as mock_save:

        user_interaction()

        # Проверяем что сохранение НЕ было вызвано
        mock_save.assert_not_called()
