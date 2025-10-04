from src.classes_api import HeadHunterAPI
from src.classes_vacancy import Vacancy, VacancyList
from src.classes_file_operations import JSONSaver


# Создание экземпляра класса для работы с API сайтов с вакансиями
hh_api = HeadHunterAPI()

# Получение вакансий с hh.ru в формате JSON
hh_vacancies = hh_api.get_vacancies("Python")
print(hh_vacancies)

# Преобразование набора данных из JSON в список объектов
# vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
my_vacancies_list = VacancyList()
vacancies_list = my_vacancies_list.add_several_vacancy_from_hh(hh_vacancies)
print(vacancies_list)

# # Пример работы конструктора класса с одной вакансией
vacancy = Vacancy.init_vacancy_manual_method("Python Developer", "<https://hh.ru/vacancy/123456>", "100000", "Требования: опыт работы от 3 лет...")
print(vacancy)
# Сохранение информации о вакансиях в файл
json_saver = JSONSaver()

# json_saver.add_vacancy_to_file(vacancy, 'test')
json_saver.add_vacancy_list_to_file(vacancies_list, 'test')
# json_saver.delete_vacancy(vacancy)
#
# # Функция для взаимодействия с пользователем
# def user_interaction():
#     platforms = ["HeadHunter"]
#     search_query = input("Введите поисковый запрос: ")
#     top_n = int(input("Введите количество вакансий для вывода в топ N: "))
#     filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
#     salary_range = input("Введите диапазон зарплат: ") # Пример: 100000 - 150000
#
#     filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
#
#     ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
#
#     sorted_vacancies = sort_vacancies(ranged_vacancies)
#     top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
#     print_vacancies(top_vacancies)
#
#
# if __name__ == "__main__":
#     user_interaction()
