import psycopg2
import os

conn_password: str = os.getenv('POSTGRES_PW')

conn = psycopg2.connect(
    host="localhost",
    database="course_5",
    user="postgres",
    password=conn_password
)

curs = conn.cursor()


class SaveToDataBase:

    def __init__(self, data):
        self.data = data

    def write_data(self) -> None:
        employers_data = self.data
        for item in employers_data:
            all_data = (
                item["vacancy_id"], item["company"],
                item["profession"], item["url"],
                item["city"], item["salary_min"], item["salary_max"],
            )
            curs.execute(f"DELETE FROM vacancies WHERE vacancy_id = {item['vacancy_id']}")
            curs.execute("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s)", all_data)
            conn.commit()


class DBManager:
    @staticmethod
    def get_companies_and_vacancies_count():
        """
        Получает список всех компаний и
        количество вакансий у каждой компании.
        """

        try:
            curs.execute("TRUNCATE TABLE company_vacancies_count")
            curs.execute("INSERT INTO company_vacancies_count(company, amount_of_vacancies) "
                         "SELECT company, COUNT(*) "
                         "FROM vacancies "
                         "GROUP BY company "
                         "ORDER BY COUNT(*) DESC")
            conn.commit()
            return f"Данные сохранены в таблицу 'company_vacancies_count'"
        except Exception as e:
            print(f"The error '{e}' occurred. Selection failed")
            conn.rollback()

    @staticmethod
    def get_all_vacancies():
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        """

        try:
            curs.execute("TRUNCATE TABLE vacancies_short")
            curs.execute("INSERT INTO vacancies_short(vacancy, company, url, salary_min) "
                         "SELECT vacancy, company, url, salary_min FROM vacancies "
                         )
            conn.commit()
            return f"Данные сохранены в таблицу 'vacancies_short'"
        except Exception as e:
            print(f"The error '{e}' occurred. Selection failed")
            conn.rollback()

    @staticmethod
    def get_avg_salary():
        """
        Получает среднюю зарплату по вакансиям.
        """

        try:
            curs.execute("TRUNCATE TABLE average_salary")
            curs.execute("INSERT INTO average_salary(company, avg_salary) "
                         "SELECT company, ROUND(AVG(salary_min)) AS average "
                         "FROM vacancies "
                         "GROUP BY company "
                         "ORDER BY ROUND(AVG(salary_min)) DESC")
            conn.commit()
            return f"Данные сохранены в таблицу 'average_salary'"
        except Exception as e:
            print(f"The error '{e}' occurred. Selection failed")
            conn.rollback()

    @staticmethod
    def get_vacancies_with_higher_salary():
        """
        Получает список всех вакансий, у которых
        зарплата выше средней по всем вакансиям.
        """

        try:
            curs.execute("TRUNCATE TABLE higher_salary")
            curs.execute("INSERT INTO higher_salary(vacancy_id, vacancy, company, url, salary_min) "
                         "SELECT vacancy_id, vacancy, company, url, salary_min FROM vacancies "
                         "WHERE salary_min > (SELECT AVG(salary_min) FROM vacancies) "
                         "ORDER BY salary_min DESC")
            conn.commit()
            return f"Данные сохранены в таблицу 'higher_salary'"
        except Exception as e:
            print(f"The error '{e}' occurred. Selection failed")
            conn.rollback()

    @staticmethod
    def get_vacancies_with_keyword(keyword):
        """
        Получает список всех вакансий, в названии которых
        содержатся переданные в метод слова.
        """

        try:
            curs.execute("TRUNCATE TABLE vacancies_with_keyword")
            curs.execute("INSERT INTO vacancies_with_keyword(vacancy_id, vacancy, company, url, salary_min) "
                         "SELECT vacancy_id, vacancy, company, url, salary_min FROM vacancies "
                         "WHERE LOWER(vacancy) LIKE %s ", ("%" + keyword + "%",))
            conn.commit()
            curs.execute("SELECT * FROM vacancies_with_keyword")
            result = curs.fetchall()
            if result in (None, [], ()):
                return f"Нет вакансий по данному ключевому слову"
            return f"Данные сохранены в таблицу 'vacancies_with_keyword'"
        except Exception as e:
            print(f"The error '{e}' occurred. Selection failed")
            conn.rollback()


class DataCleaner:
    @staticmethod
    def delete_all_data():
        try:
            curs.execute("TRUNCATE TABLE vacancies")
        except Exception as e:
            print(f"The error '{e}' occurred.")
            conn.rollback()
