from src.classes_api import HeadHunterAPI
from src.classes_vacancy import VacancyList
from src.classes_file_operations import JSONSaver
from src.db_connect import DBManager
import json
from src.config import config


params = config('database.ini')
name_db = 'headhunter'
my_emp = [
        '1740', # 1. Яндекс
        '104628', # 2. Газпром
        '1373', # 3. Аэрофлот
        '15478', # 4. VK
        '680183', # 5. LUKOIL International
        '9853364', # 6. АНО Роскосмос Медиа
        '577743', # 7. Госкорпорация Росатом
        '4934', # 8. Билайн
        '193400', # 9. АВТОВАЗ
        '3776', # 10. МТС
    ]

# my_emp = [
#         {'id': '1740', 'name': 'Яндекс', 'url': ''},
#         {'id': '104628', 'name': 'Газпром', 'url': ''},
#         {'id': '1373', 'name': 'Аэрофлот', 'url': ''},
#         {'id': '15478', 'name': 'VK', 'url': ''},
#         {'id': '680183', 'name': 'LUKOIL International', 'url': ''},
#         {'id': '9853364', 'name': 'АНО Роскосмос Медиа', 'url': ''},
#         {'id': '577743', 'name': 'Госкорпорация Росатом', 'url': ''},
#         {'id': '4934', 'name': 'Билайн', 'url': ''},
#         {'id': '193400', 'name': 'АВТОВАЗ', 'url': ''},
#         {'id': '3776', 'name': 'МТС', 'url': ''}
#     ]

# # Функция для взаимодействия с пользователем
# def user_interaction():
#
#     # Tests variable
#     # search_query = 'python'
#     # len_vacancy_api_res = 50
#     # filter_words = 'опыт json'.split()
#     # salary_range = '10000 - 100000'
#     # flag_sort_salary = 'y'
#     # top_n_res = 10
#
#     # Получаем запрос поиска и количество полученных ответов от HH
#     search_query = input('Введите поисковый запрос: ')
#     len_vacancy_api_res = input('Введите количество вакансий для получения от HH : ')
#
#     # Создание экземпляра класса для работы с API сайтов с вакансиями
#     hh_api = HeadHunterAPI()
#     # Получение вакансий с hh.ru в формате JSON
#     hh_vacancies = hh_api.get_vacancies(search_query, per_page=len_vacancy_api_res)
#
#     # Создаем объект для нашего приложения
#     my_vacancy_list = VacancyList()
#     # Добавляем полученные вакансии
#     my_vacancy_list.add_several_vacancy_from_hh(hh_vacancies)
#
#     # Получаем ключевые слова и фильтруем вакансии по ключевым словам
#     filter_words = input('Введите ключевые слова для фильтрации вакансий: ').split()
#     my_vacancy_list = my_vacancy_list.filter_by_req(filter_words)
#
#     # Получаем диапазон зарплат фильтруем вакансии в диапазоне зарплат
#     salary_range = input('Введите диапазон зарплат: ')
#     my_vacancy_list = my_vacancy_list.filter_by_salary(salary_range)
#
#     # Предлагаем отсортировать вакансии по зарплате
#     flag_sort_salary = input('Отсортировать вакансии по зарплате? Y/N: ').lower()
#     if flag_sort_salary == 'y':
#         my_vacancy_list = my_vacancy_list.sorted_by_salary(False)
#
#     # Получаем количество для вывода результатов и выводим указанное количество вакансий
#     top_n_res = input('Введите количество вакансий для вывода: ')
#     top_vacancies = my_vacancy_list.get_top_vacancies(top_n_res)
#     print(top_vacancies.vacancy_list)
#
#     # Предлагаем записать результаты работы в файл
#     flag_save_json_file = input('Записать результаты работы в файл? Y/N: ').lower()
#     if flag_save_json_file == 'y':
#         file_name = input('Введите имя файла: ')
#         json_saver = JSONSaver(file_name)
#         json_saver.add_vacancy_list_to_file(top_vacancies)
#         print(f'Данные записаны в файл {file_name}, в папке data')
#
#     print('Программа успешно завершила свою работу')


def main():
    hh_api = HeadHunterAPI()

    data_vacancies = hh_api.get_vacancies('', employer_ids=my_emp, per_page='100')


    db_connect = DBManager(params)
    db_connect.create_db(name_db)





if __name__ == '__main__':
    # user_interaction()
    main()