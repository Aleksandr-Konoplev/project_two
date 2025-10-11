from src.classes_api import HeadHunterAPI
from src.classes_vacancy import VacancyList
from src.classes_file_operations import JSONSaver


# Функция для взаимодействия с пользователем
def user_interaction():

    # Tests variable
    # search_query = 'python'
    # len_vacancy_api_res = 50
    # filter_words = 'опыт json'.split()
    # salary_range = '10000 - 100000'
    # flag_sort_salary = 'y'
    # top_n_res = 10

    # Получаем запрос поиска и количество полученных ответов от HH
    search_query = input('Введите поисковый запрос: ')
    len_vacancy_api_res = int(input('Введите количество вакансий для получения от HH : '))

    # Создание экземпляра класса для работы с API сайтов с вакансиями
    hh_api = HeadHunterAPI()
    # Получение вакансий с hh.ru в формате JSON
    hh_vacancies = hh_api.get_vacancies(search_query, per_page=len_vacancy_api_res)

    # Создаем объект для нашего приложения
    my_vacancy_list = VacancyList()
    # Добавляем полученные вакансии
    my_vacancy_list.add_several_vacancy_from_hh(hh_vacancies)

    # Получаем ключевые слова и фильтруем вакансии по ключевым словам
    filter_words = input('Введите ключевые слова для фильтрации вакансий: ').split()
    my_vacancy_list = my_vacancy_list.filter_by_req(filter_words)

    # Получаем диапазон зарплат фильтруем вакансии в диапазоне зарплат
    salary_range = input('Введите диапазон зарплат: ')
    my_vacancy_list = my_vacancy_list.filter_by_salary(salary_range)

    # Предлагаем отсортировать вакансии по зарплате
    flag_sort_salary = input('Отсортировать вакансии по зарплате? Y/N: ').lower()
    if flag_sort_salary == 'y':
        my_vacancy_list = my_vacancy_list.sorted_by_salary(False)

    # Получаем количество для вывода результатов и выводим указанное количество вакансий
    top_n_res = int(input('Введите количество вакансий для вывода: '))
    top_vacancies = my_vacancy_list.get_top_vacancies(top_n_res)
    print(top_vacancies.vacancy_list)

    # Предлагаем записать результаты работы в файл
    flag_save_json_file = input('Записать результаты работы в файл? Y/N: ').lower()
    if flag_save_json_file == 'y':
        file_name = input('Введите имя файла: ')
        json_saver = JSONSaver()
        json_saver.add_vacancy_list_to_file(my_vacancy_list, file_name)
        print(f'Данные записаны в файл {file_name}, в папке data')


if __name__ == '__main__':
    user_interaction()
