import json
import os
from abc import ABC, abstractmethod

from src.classes_vacancy import Vacancy, VacancyList

# Получаем абсолютную ссылку к корню проекта
folder_data = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\data\\'


class ConnectFile(ABC):

    @staticmethod
    @abstractmethod
    def save_vacancies_to_file(vacancy_list, file_name):
        """ Сохраняет список вакансий в новый файл """
        pass

    @staticmethod
    @abstractmethod
    def add_vacancy_to_file(vacancy, file_name):
        """ Добавляет одну вакансию в файл """
        pass

    @staticmethod
    @abstractmethod
    def add_vacancy_list_to_file(vacancy_list, file_name):
        """ Добавляет список вакансий в файл """
        pass

    @staticmethod
    @abstractmethod
    def del_vacancy_from_file(vacancy, file_name):
        """ Удаляет вакансию из файла """
        pass

    @abstractmethod
    def search_vacancy(self):
        """ Ищет вакансию в файле """
        pass


class JSONSaver(ConnectFile):

    def __init__(self, file_n='vacancy'):
        if isinstance(file_n, str) and file_n not in ('', ' '):
            self.__file_name = file_n + '.json'
        else:
            self.__file_name = 'vacancy' + '.json'

    def save_vacancies_to_file(self, vacancy_list_obj):
        """ Сохраняет список вакансий (полученный в виде объекта класса VacancyList) в новый файл """
        if isinstance(vacancy_list_obj, VacancyList):
            vacancy_list_dict = []
            for vacancy in vacancy_list_obj.vacancy_list:
                vacancy_list_dict.append({
                    'id': vacancy.vacancy_id,
                    'name': vacancy.name,
                    'url': vacancy.url,
                    'salary': vacancy.salary,
                    'requirement': vacancy.requirement
                })

            with open(folder_data + self.__file_name, 'w', encoding='utf-8') as f:
                json.dump(vacancy_list_dict, f, ensure_ascii=False, indent=4)

    def add_vacancy_to_file(self, vacancy):
        """ Добавляет одну вакансию в файл """
        if os.path.exists(folder_data + self.__file_name):  # Проверяем существует ли файл
            with open(folder_data + self.__file_name, 'r', encoding='utf-8') as f:
                try:
                    data_file = json.load(f)
                except json.JSONDecodeError:
                    data_file = []
        else:
            data_file = []
        data_file.append({
            'id': vacancy.vacancy_id,
            'name': vacancy.name,
            'url': vacancy.url,
            'salary': vacancy.salary,
            'requirement': vacancy.requirement
        })

        with open(folder_data + self.__file_name, 'w', encoding='utf-8') as f:
            json.dump(data_file, f, ensure_ascii=False, indent=4)

    def add_vacancy_list_to_file(self, vacancy_list):
        """ Добавляет список вакансий в файл """
        if os.path.exists(folder_data + self.__file_name):  # Проверяем существует ли файл
            with open(folder_data + self.__file_name, 'r', encoding='utf-8') as f:
                try:
                    data_file = json.load(f)
                except json.JSONDecodeError:
                    data_file = []
        else:
            data_file = []

        if isinstance(vacancy_list, VacancyList):
            for vacancy in vacancy_list.vacancy_list:
                data_file.append({
                    'id': vacancy.vacancy_id,
                    'name': vacancy.name,
                    'url': vacancy.url,
                    'salary': vacancy.salary,
                    'requirement': vacancy.requirement
                })

        with open(folder_data + self.__file_name, 'w', encoding='utf-8') as f:
            json.dump(data_file, f, ensure_ascii=False, indent=4)

    def del_vacancy_from_file(self, vacancy):
        """
        Удаляет вакансию из файла, поиск проводится по совпадению ссылки,
        так как вакансия может быть создана вручную и не иметь ID.
        """
        if isinstance(vacancy, Vacancy):
            file_path = folder_data + self.__file_name

            # Проверяем наличие файла
            if not os.path.exists(file_path):
                print(f'Файл {file_path} не найден.')
                return None

            # Загружаем текущие данные
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    print('Ошибка чтения файла JSON.')
                    return None

            # Добавляем все вакансии кроме удаляемой.
            new_data = [v for v in data if not (v['url'] == vacancy.url)]

            # Проверяем, была ли вакансия удалена
            if len(new_data) == len(data):
                print('Вакансия не найдена в файле.')
            else:
                print(f'Вакансия "{vacancy.name}" успешно удалена.')

            # Перезаписываем файл
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, indent=4, ensure_ascii=False)
                return None

        else:
            raise TypeError('Удаляемый элемент не принадлежит к классу Vacancy, удаление невозможно')

    def get_file_path(self):
        """Возвращает полный путь к JSON-файлу"""
        return os.path.join(folder_data, self.__file_name)

    def search_vacancy(self):
        """ Ищет вакансию в файле """
        pass
