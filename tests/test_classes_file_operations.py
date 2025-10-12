import json
import os

import pytest

from src.classes_file_operations import JSONSaver


def test_save_vacancies_to_file_creates_new_file(sample_vacancy_list, temp_json_file):
    saver = JSONSaver(temp_json_file)
    path = saver.get_file_path()

    # Убедимся, что файла нет
    if os.path.exists(path):
        os.remove(path)

    saver.save_vacancies_to_file(sample_vacancy_list)

    assert os.path.exists(path)

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    assert isinstance(data, list)
    assert len(data) == len(sample_vacancy_list.vacancy_list)
    assert data[0]['name'] == sample_vacancy_list.vacancy_list[0].name

    os.remove(path)


def test_add_vacancy_to_file(sample_vacancy, temp_json_file):
    saver = JSONSaver(temp_json_file)
    path = saver.get_file_path()

    with open(path, 'w', encoding='utf-8') as f:
        json.dump([], f)

    saver.add_vacancy_to_file(sample_vacancy)

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    assert len(data) == 1
    assert data[0]['url'] == sample_vacancy.url

    os.remove(path)


def test_add_vacancy_list_to_file(sample_vacancy_list, temp_json_file):
    saver = JSONSaver(temp_json_file)
    path = saver.get_file_path()

    # Создаем файл с одной старой записью
    with open(path, 'w', encoding='utf-8') as f:
        json.dump([{'id': 'old', 'name': 'OldVacancy', 'url': 'old_url', 'salary': 100, 'requirement': 'none'}], f)

    saver.add_vacancy_list_to_file(sample_vacancy_list)

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # старая + новые вакансии
    assert len(data) == len(sample_vacancy_list.vacancy_list) + 1
    assert any(v['name'] == 'Data Engineer' for v in data)

    os.remove(path)


def test_add_vacancy_to_file_creates_if_missing(sample_vacancy, temp_json_file):
    saver = JSONSaver(temp_json_file)
    path = saver.get_file_path()

    if os.path.exists(path):
        os.remove(path)

    saver.add_vacancy_to_file(sample_vacancy)

    assert os.path.exists(path)
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    assert len(data) == 1

    os.remove(path)


def test_del_vacancy_from_file_success(sample_vacancy, temp_json_file):
    saver = JSONSaver(temp_json_file)
    path = saver.get_file_path()

    # создаем файл с двумя вакансиями
    data = [
        {
            'id': '123', 'name': 'Python Developer',
            'url': 'https://hh.ru/vacancy/123',
            'salary': 100000, 'requirement': 'test'
        },
        {
            'id': '124', 'name': 'Data Engineer',
            'url': 'https://hh.ru/vacancy/999',
            'salary': 200000, 'requirement': 'req2'
        }
    ]
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f)

    saver.del_vacancy_from_file(sample_vacancy)

    with open(path, 'r', encoding='utf-8') as f:
        new_data = json.load(f)

    assert len(new_data) == 1
    assert all(v['url'] != sample_vacancy.url for v in new_data)

    os.remove(path)


def test_del_vacancy_from_file_not_found(sample_vacancy, temp_json_file, capsys):
    saver = JSONSaver(temp_json_file)
    path = saver.get_file_path()

    with open(path, 'w', encoding='utf-8') as f:
        json.dump([], f)

    saver.del_vacancy_from_file(sample_vacancy)
    captured = capsys.readouterr()
    assert "не найдена" in captured.out

    os.remove(path)


def test_del_vacancy_from_file_invalid_type(temp_json_file):
    saver = JSONSaver(temp_json_file)
    with pytest.raises(TypeError):
        saver.del_vacancy_from_file({"not": "a vacancy"})


def test_del_vacancy_from_file_file_missing(sample_vacancy, temp_json_file, capsys):
    saver = JSONSaver(temp_json_file)
    path = saver.get_file_path()

    if os.path.exists(path):
        os.remove(path)

    saver.del_vacancy_from_file(sample_vacancy)
    captured = capsys.readouterr()
    assert "не найден" in captured.out


def test_add_vacancy_list_to_file_invalid_json(sample_vacancy_list, temp_json_file):
    saver = JSONSaver(temp_json_file)
    path = saver.get_file_path()

    with open(path, 'w', encoding='utf-8') as f:
        f.write('INVALID_JSON')

    saver.add_vacancy_list_to_file(sample_vacancy_list)

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    assert isinstance(data, list)
    assert len(data) == len(sample_vacancy_list.vacancy_list)

    os.remove(path)


def test_add_vacancy_to_file_invalid_json(sample_vacancy, temp_json_file):
    saver = JSONSaver(temp_json_file)
    path = saver.get_file_path()

    with open(path, 'w', encoding='utf-8') as f:
        f.write('INVALID_JSON')

    saver.add_vacancy_to_file(sample_vacancy)

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    assert len(data) == 1

    os.remove(path)
