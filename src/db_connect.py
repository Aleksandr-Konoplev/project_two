from abc import ABC, abstractmethod
import psycopg2
from psycopg2 import Error, sql
from typing import Any


class AbstractDBM(ABC):

    def __init__(self, conf_db_file: str):
        """ Инициация подключения к БД """
        pass

    @abstractmethod
    def create_db(self, db_name):
        """  Создание БД"""
        pass

    @abstractmethod
    def read_db(self):
        """ Чтение БД """
        pass

    @abstractmethod
    def update_db(self):
        """ Обновление БД """
        pass

    @abstractmethod
    def delete_db(self, db_name):
        """ Удаление из БД """
        pass

    @abstractmethod
    def get_companies_and_vacancies_count(self):
        """ Получает список всех компаний и количество вакансий у каждой компании """
        pass

    @abstractmethod
    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
        pass

    @abstractmethod
    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям"""
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""
        pass


class DBManager(AbstractDBM):

    def __init__(self, params: dict[str, str], db_name: str | None = None):
        """
        Конструктор класса DBManager.
        1. Читает параметры подключения к БД из файла конфигурации.
        2. Проверяет, существует ли база данных.
        3. Создаёт базу данных, если её нет.
        4. Подключается к указанной базе данных.

        :param params: Путь к файлу конфигурации с параметрами подключения
        :param db_name: имя базы данных для подключения
        """

        self.params = params

        # Инициализируем соединение и курсор
        self.conn = None
        self.cur = None

        # Если указано имя базы данных
        if db_name:
            # Добавляем имя базы в параметры
            self.params['database'] = db_name

        try:
            self.conn = psycopg2.connect(**self.params)
            self.cur = self.conn.cursor()
            print(f'Подключение к базе данных "{self.params.get("database", "no name")}" установлено.')
        except Error as e:
            print(f'Ошибка подключения к БД: {e}')

    def create_db(self, db_name: str):
        """Создание базы данных и таблиц, если их нет."""
        try:
            # Подключаемся к "postgres" без имени БД
            temp_params = self.params.copy()
            temp_params.pop('database', None)
            conn = psycopg2.connect(**temp_params)
            conn.autocommit = True  # важное место: CREATE DATABASE вне транзакции
            cur = conn.cursor()

            # Проверяем, существует ли база
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
            exists = cur.fetchone()
            if not exists:
                cur.execute(f'CREATE DATABASE "{db_name}"')
                print(f'База данных "{db_name}" успешно создана.')
            else:
                print(f'База данных "{db_name}" уже существует.')

            cur.close()
            conn.close()

            # Подключаемся к новой или существующей базе
            self.params['database'] = db_name
            self.conn = psycopg2.connect(**self.params)
            self.conn.autocommit = True
            self.cur = self.conn.cursor()

            # Создаем таблицы
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS employers (
                    employer_id VARCHAR PRIMARY KEY,
                    employer_name VARCHAR NOT NULL,
                    employer_url TEXT
                );
            """)

            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    vacancy_id VARCHAR PRIMARY KEY,
                    vacancy_name VARCHAR NOT NULL,
                    vacancy_url TEXT,
                    employer_id VARCHAR REFERENCES employers(employer_id) ON DELETE CASCADE,
                    area_id INT,
                    salary INT
                );
            """)

            print(f'Таблицы в базе данных "{db_name}" созданы.')

        except Error as e:
            print(f'Ошибка при создании БД или таблиц: {e}')

    def read_db(self):
        """ Чтение БД """
        pass

    def update_db(self):
        """ Обновление БД """
        pass

    def update_employers(self, id_list_emp: list[str], ):
        """ Обновление таблицы работодателей """
        for emp in id_list_emp:
            self.cur.execute(
                """
                INSERT INTO employers (employer_id, employer_name, employer_url)
                VALUES (%s, %s, %s)
                """,
                (emp, emp['name'], emp['url'])
            )




    def delete_db(self, db_name: str):
        """Удаление базы данных с отключением всех подключений к ней."""
        try:
            # Подключаемся к временной базе, например 'postgres'
            temp_params = self.params.copy()
            temp_params.pop('database', None)
            conn = psycopg2.connect(**temp_params)
            conn.autocommit = True
            cur = conn.cursor()

            # Завершаем все активные соединения с целевой базой
            cur.execute(f"""
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = %s
                  AND pid <> pg_backend_pid();
            """, (db_name,))

            # Удаляем базу
            cur.execute(f'DROP DATABASE IF EXISTS "{db_name}"')
            print(f'База данных "{db_name}" успешно удалена.')

            cur.close()
            conn.close()

        except Error as e:
            print(f'Ошибка при удалении базы данных: {e}')

    def get_companies_and_vacancies_count(self):
        """ Получает список всех компаний и количество вакансий у каждой компании """
        pass

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
        pass

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям"""
        pass

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        pass

    def get_vacancies_with_keyword(self):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""
        pass
        

