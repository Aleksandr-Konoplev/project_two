import pytest
from src.classes_vacancy import Vacancy, VacancyList


# Тесты для класса Vacancy
def test_vacancy_init(fixture_vacancy_data_full):
    """
    Проверяем, что при создании объекта Vacancy из словаря:
    - все поля корректно инициализируются;
    - зарплата считается как среднее между 'from' и 'to';
    - описание корректно извлекается.
    """
    vacancy = Vacancy(fixture_vacancy_data_full)
    assert vacancy.vacancy_id == "123"
    assert vacancy.name == "Python Developer"
    assert vacancy.url == "https://hh.ru/vacancy/123"
    assert vacancy.salary == 125000
    assert "Django" in vacancy.requirement


@pytest.mark.parametrize(
    "salary_dict,expected",
    [
        # если salary = None
        (None, 0),
        # обе границы отсутствуют
        ({"from": None, "to": None}, 0),
        # обе границы заданы
        ({"from": 100000, "to": 150000}, 125000),
        # только нижняя граница
        ({"from": 100000, "to": None}, 100000),
        # только верхняя граница
        ({"from": None, "to": 200000}, 200000)
    ],
)
def test_parse_salary_cases(salary_dict, expected):
    """
    Проверяем работу приватного метода __parse_salary.
    Достаём его через getattr(), чтобы избежать ошибок IDE.
    """
    parse_salary = getattr(Vacancy, "_Vacancy__parse_salary")
    result = parse_salary(salary_dict)
    assert result == expected


def test_vacancy_manual_init():
    """
    Проверяем работу метода init_vacancy_manual_method —
    он создаёт объект Vacancy из данных, введённых вручную.
    """
    vacancy = Vacancy.init_vacancy_manual_method(
        name="QA Engineer",
        url="https://hh.ru/vacancy/789",
        salary=90000,
        requirement="Тестирование, Pytest",
        vacancy_id="manual"
    )

    # Проверяем, что вернулся именно объект Vacancy с нужными значениями
    assert isinstance(vacancy, Vacancy)
    assert vacancy.name == "QA Engineer"
    assert vacancy.salary == 90000
    assert vacancy.vacancy_id == "manual"


def test_salary_setter_valid(fixture_vacancy_data_partial):
    """
    Проверяем сеттер зарплаты — он должен позволять
    менять зарплату, если значение корректное (положительное число).
    """
    vacancy = Vacancy(fixture_vacancy_data_partial)
    vacancy.salary = 120000
    assert vacancy.salary == 120000


@pytest.mark.parametrize("invalid_salary", [-100, "abc", None])
def test_salary_setter_invalid(fixture_vacancy_data_partial, invalid_salary):
    """
    Проверяем, что при попытке установить некорректную зарплату:
    - отрицательное число
    - строку
    - None
    — выбрасывается ValueError.
    """
    vacancy = Vacancy(fixture_vacancy_data_partial)
    with pytest.raises(ValueError):
        vacancy.salary = invalid_salary


def test_requirement_setter_valid(fixture_vacancy_data_partial):
    """
    Проверяем, что можно изменить описание вакансии (requirement),
    если новое значение — строка.
    """
    vacancy = Vacancy(fixture_vacancy_data_partial)
    vacancy.requirement = "Новый стек технологий"
    assert vacancy.requirement == "Новый стек технологий"


def test_requirement_setter_invalid(fixture_vacancy_data_partial):
    """
    Проверяем, что при попытке задать описание не строкового типа
    выбрасывается TypeError.
    """
    vacancy = Vacancy(fixture_vacancy_data_partial)
    with pytest.raises(TypeError):
        vacancy.requirement = 12345


# Тесты для класса VacancyList
def test_add_one_vacancy(fixture_vacancy_data_full):
    """
    Проверяем метод add_one_vacancy:
    - можно добавить объект Vacancy;
    - он действительно появляется в списке.
    """
    v = Vacancy(fixture_vacancy_data_full)
    v_list = VacancyList()
    v_list.add_one_vacancy(v)
    assert len(v_list.vacancy_list) == 1
    assert v_list.vacancy_list[0].name == "Python Developer"


def test_add_one_vacancy_invalid_type():
    """
    Проверяем, что при попытке добавить не-объект Vacancy
    выбрасывается TypeError.
    """
    v_list = VacancyList()
    with pytest.raises(TypeError):
        v_list.add_one_vacancy("Not a Vacancy")


def test_add_several_vacancy(fixture_vacancy_data_full, fixture_vacancy_data_partial):
    """
    Проверяем добавление сразу нескольких вакансий —
    список должен увеличиться на 2 элемента.
    """
    v1 = Vacancy(fixture_vacancy_data_full)
    v2 = Vacancy(fixture_vacancy_data_partial)
    v_list = VacancyList()
    v_list.add_several_vacancy([v1, v2])
    assert len(v_list.vacancy_list) == 2


def test_add_several_vacancy_invalid():
    """
    Проверяем, что если хотя бы один элемент не является Vacancy,
    метод выбрасывает TypeError.
    """
    v_list = VacancyList()
    with pytest.raises(TypeError):
        v_list.add_several_vacancy(["abc", 123])


def test_add_one_vacancy_from_hh(fixture_vacancy_data_full):
    """
    Проверяем метод add_one_vacancy_from_hh:
    - принимает словарь от HH API,
    - создаёт объект Vacancy внутри,
    - добавляет его в список.
    """
    v_list = VacancyList()
    result = v_list.add_one_vacancy_from_hh(fixture_vacancy_data_full)
    assert isinstance(result, VacancyList)
    assert len(v_list.vacancy_list) == 1
    assert isinstance(v_list.vacancy_list[0], Vacancy)


def test_add_several_vacancy_from_hh(fixture_vacancy_data_full, fixture_vacancy_data_partial):
    """
    Проверяем добавление сразу нескольких вакансий из списка словарей HH API.
    """
    v_list = VacancyList()
    result = v_list.add_several_vacancy_from_hh([fixture_vacancy_data_full, fixture_vacancy_data_partial])
    assert isinstance(result, VacancyList)
    assert len(v_list.vacancy_list) == 2
    assert all(isinstance(v, Vacancy) for v in v_list.vacancy_list)


def test_sorted_by_salary(fixture_vacancy_data_full, fixture_vacancy_data_partial):
    """
    Проверяем сортировку списка вакансий по зарплате.
    Ожидаем, что вакансии будут отсортированы по возрастанию.
    """
    v1 = Vacancy(fixture_vacancy_data_full)   # зарплата = 125000
    v2 = Vacancy(fixture_vacancy_data_partial)  # зарплата = 80000
    v_list = VacancyList()
    v_list.add_several_vacancy([v1, v2])

    sorted_list = v_list.sorted_by_salary()

    # Проверяем, что сортировка от меньшего к большему
    assert [v.salary for v in sorted_list] == [125000, 80000]
