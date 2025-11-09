from abc import ABC, abstractmethod

import psycopg2
from psycopg2 import Error


class AbstractDBM(ABC):

    @abstractmethod
    def __init__(self, params, db_name):
        """ Инициация подключения к БД """
        self.db_name = db_name
        self.params = params

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
        """получает список всех вакансий с указанием компании, названия вакансии и зарплаты и ссылки на вакансию"""
        pass

    @abstractmethod
    def get_avg_salary(self, db_name):
        """получает среднюю зарплату по вакансиям"""
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self, var_salary):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self, keyword: str):
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

        super().__init__(params, db_name)
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

    def update_db(self, employers_data: list[dict] | None = None, vacancies_data: list[dict] | None = None):
        """
        Универсальное обновление данных в БД:
        - обновляет таблицу работодателей (employers)
        - обновляет таблицу вакансий (vacancies)

        :param employers_data: список работодателей (dict с ключами id, name, url)
        :param vacancies_data: список вакансий (dict с ключами id, name, url, employer_id, area_id, salary)
        """
        try:
            if employers_data:
                print("Обновляю таблицу работодателей...")
                self.update_employers(employers_data)

            if vacancies_data:
                print("Обновляю таблицу вакансий...")
                self.update_vacancies(vacancies_data)

            self.conn.commit()
            print("Обновление базы данных завершено успешно.")

        except Error as e:
            self.conn.rollback()
            print(f"Ошибка при обновлении базы данных: {e}")

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
            cur.execute("""
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

    def update_employers(self, employers_data: list[dict]):
        """Обновление таблицы работодателей (вставка или обновление при совпадении ID)."""
        for emp in employers_data:
            self.cur.execute(
                """
                INSERT INTO employers (employer_id, employer_name, employer_url)
                VALUES (%s, %s, %s)
                ON CONFLICT (employer_id) DO UPDATE
                SET employer_name = EXCLUDED.employer_name,
                    employer_url = EXCLUDED.employer_url;
                """,
                (emp['id'], emp['name'], emp['url'])
            )

    def update_vacancies(self, vacancies_data: list[dict]):
        """Обновление таблицы вакансий (вставка или обновление при совпадении ID)."""
        for vac in vacancies_data:
            self.cur.execute(
                """
                INSERT INTO vacancies (vacancy_id, vacancy_name, vacancy_url, employer_id, area_id, salary)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (vacancy_id) DO UPDATE
                SET vacancy_name = EXCLUDED.vacancy_name,
                    vacancy_url = EXCLUDED.vacancy_url,
                    employer_id = EXCLUDED.employer_id,
                    area_id = EXCLUDED.area_id,
                    salary = EXCLUDED.salary;
                """,
                (
                    vac['id'],
                    vac['name'],
                    vac['url'],
                    vac.get('employer', {}).get('id'),
                    vac.get('area', {}).get('id'),
                    vac.get('salary', {}).get('from') if vac.get('salary') else None
                )
            )

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.

        :return: Список кортежей (employer_name, vacancies_count)
        """
        try:
            self.cur.execute("""
                SELECT e.employer_name, COUNT(v.vacancy_id) AS vacancies_count
                FROM employers e
                LEFT JOIN vacancies v ON e.employer_id = v.employer_id
                GROUP BY e.employer_name
                ORDER BY vacancies_count DESC, e.employer_name;
            """)

            results = self.cur.fetchall()

            if not results:
                print("В базе данных нет данных о компаниях или вакансиях.")
                return []

            print(f"Найдено {len(results)} компаний.")
            return results

        except Error as e:
            print(f"Ошибка при получении количества вакансий по компаниям: {e}")
            return []

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием:
        - названия компании,
        - названия вакансии,
        - зарплаты,
        - ссылки на вакансию.

        :return: Список кортежей (employer_name, vacancy_name, salary, vacancy_url)
        """
        try:
            self.cur.execute("""
                SELECT e.employer_name, v.vacancy_name, v.salary, v.vacancy_url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
                ORDER BY e.employer_name, v.salary DESC NULLS LAST;
            """)

            results = self.cur.fetchall()

            if not results:
                print("В базе данных нет вакансий.")
                return []

            print(f"Всего найдено {len(results)} вакансий.")
            return results

        except Error as e:
            print(f"Ошибка при получении списка всех вакансий: {e}")
            return []

    def get_avg_salary(self, db_name):
        """Получает среднюю зарплату по всем вакансиям."""
        try:
            self.params['database'] = db_name
            self.conn = psycopg2.connect(**self.params)
            self.cur.execute("SELECT AVG(salary) FROM vacancies WHERE salary IS NOT NULL;")
            avg_salary = self.cur.fetchone()[0]

            if avg_salary is None:
                print("В базе данных нет данных о зарплате.")
                return None

            print(f"Средняя зарплата по всем вакансиям: {round(avg_salary)}")
            return round(avg_salary, 2)

        except Error as e:
            print(f"Ошибка при получении средней зарплаты: {e}")
            return None

    def get_vacancies_with_higher_salary(self, var_salary: int | float):
        """
        Получает список всех вакансий, у которых зарплата выше переданной.
        :param var_salary: Зарплата, с которой нужно сравнивать
        :return: Список кортежей (vacancy_name, employer_name, salary, vacancy_url)
        """
        try:
            self.cur.execute("""
                SELECT v.vacancy_name, e.employer_name, v.salary, v.vacancy_url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
                WHERE v.salary IS NOT NULL AND v.salary > %s
                ORDER BY v.salary DESC;
            """, (var_salary,))

            results = self.cur.fetchall()

            if not results:
                print(f"Нет вакансий с зарплатой выше {var_salary}.")
                return []

            print(f"Найдено {len(results)} вакансий с зарплатой выше {var_salary}.")
            return results

        except Error as e:
            print(f"Ошибка при получении вакансий с зарплатой выше {var_salary}: {e}")
            return []

    def get_vacancies_with_keyword(self, keyword: str):
        """
        Получает список всех вакансий, в названии которых содержится переданное слово.
        Поиск нечувствителен к регистру.

        :param keyword: Ключевое слово для поиска (например, 'python')
        :return: список кортежей (vacancy_name, employer_name, salary, vacancy_url)
        """
        try:
            self.cur.execute("""
                SELECT v.vacancy_name, e.employer_name, v.salary, v.vacancy_url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
                WHERE LOWER(v.vacancy_name) LIKE %s
                ORDER BY v.salary DESC NULLS LAST;
            """, (f"%{keyword.lower()}%",))

            results = self.cur.fetchall()

            if not results:
                print(f'Вакансий с ключевым словом "{keyword}" не найдено.')
                return []

            print(f'Найдено {len(results)} вакансий, содержащих "{keyword}".')
            return results

        except Error as e:
            print(f'Ошибка при поиске вакансий с ключевым словом "{keyword}": {e}')
            return []
