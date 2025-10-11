import json
import os

import pytest

from src.classes_file_operations import JSONSaver
from src.classes_vacancy import Vacancy, VacancyList


def test_save_vacancies_to_file_creates_new_file(sample_vacancy_list, temp_json_file):
    """
    Проверяем, что метод save_vacancies_to_file создаёт новый файл и корректно сохраняет список вакансий.
    """
    JSONSaver.save_vacancies_to_file(sample_vacancy_list, os.path.basename(temp_json_file))

    # Проверяем, что файл действительно существует
    folder_data = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\data\\'
    file_path = folder_data + os.path.basename(temp_json_file)
    assert os.path.exists(file_path)

    # Проверяем содержимое
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert isinstance(data, list)
        assert data[0]["name"] == "Python Developer"
        assert data[0]["salary"] == 150000

    # Удаляем тестовый файл
    os.remove(file_path)


def test_add_vacancy_to_file_creates_and_appends(sample_vacancy, temp_json_file):
    """
    Проверяем, что метод add_vacancy_to_file корректно создаёт новый файл, если его нет,
    и добавляет вакансию в существующий файл.
    """
    folder_data = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\data\\'
    file_name = os.path.basename(temp_json_file)
    file_path = folder_data + file_name

    # Добавляем первую вакансию
    JSONSaver.add_vacancy_to_file(sample_vacancy, file_name)

    # Проверяем, что файл создан
    assert os.path.exists(file_path)

    # Добавляем вторую вакансию
    JSONSaver.add_vacancy_to_file(sample_vacancy, file_name)

    # Проверяем, что теперь в файле две записи
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert len(data) == 2

    os.remove(file_path)


def test_add_vacancy_list_to_file_appends_multiple(sample_vacancy_list, temp_json_file):
    """
    Проверяем, что метод add_vacancy_list_to_file добавляет несколько вакансий в файл.
    """
    folder_data = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\data\\'
    file_name = os.path.basename(temp_json_file)
    file_path = folder_data + file_name

    # Добавляем один и тот же список дважды
    JSONSaver.add_vacancy_list_to_file(sample_vacancy_list, file_name)
    JSONSaver.add_vacancy_list_to_file(sample_vacancy_list, file_name)

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert len(data) == 2
        assert all("Python Developer" in v["name"] for v in data)

    os.remove(file_path)


def test_del_vacancy_from_file_removes_entry(sample_vacancy, sample_vacancy_list, temp_json_file):
    """
    Проверяем, что метод del_vacancy_from_file действительно удаляет вакансию по URL.
    """
    folder_data = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\data\\'
    file_name = os.path.basename(temp_json_file)
    file_path = folder_data + file_name

    # Сначала сохраняем вакансию
    JSONSaver.save_vacancies_to_file(sample_vacancy_list, file_name)

    # Проверяем, что вакансия в файле
    with open(file_path, "r", encoding="utf-8") as f:
        data_before = json.load(f)
        assert len(data_before) == 1

    # Удаляем вакансию
    saver = JSONSaver()
    saver.del_vacancy_from_file(sample_vacancy, file_name)

    # Проверяем, что файл теперь пуст
    with open(file_path, "r", encoding="utf-8") as f:
        data_after = json.load(f)
        assert len(data_after) == 0

    os.remove(file_path)


def test_del_vacancy_from_file_not_found(sample_vacancy, temp_json_file, capsys):
    """
    Проверяем поведение при попытке удалить вакансию, которой нет в файле.
    """
    folder_data = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\data\\'
    file_name = os.path.basename(temp_json_file)
    file_path = folder_data + file_name

    # Сохраняем другую вакансию
    v_list = VacancyList()
    v_list.add_one_vacancy(Vacancy.init_vacancy_manual_method(
        "Java Dev",
        "https://hh.ru/vacancy/456",
        100000,
        "Spring")
    )
    JSONSaver.save_vacancies_to_file(v_list, file_name)

    # Пытаемся удалить Python Developer (её нет в файле)
    saver = JSONSaver()
    saver.del_vacancy_from_file(sample_vacancy, file_name)

    # Читаем вывод функции
    captured = capsys.readouterr()
    assert "не найдена" in captured.out.lower()

    os.remove(file_path)


def test_del_vacancy_from_file_invalid_type_raises(temp_json_file):
    """
    Проверяем, что при передаче не Vacancy вызывается исключение TypeError.
    """
    saver = JSONSaver()
    with pytest.raises(TypeError):
        saver.del_vacancy_from_file("не объект Vacancy", os.path.basename(temp_json_file))
