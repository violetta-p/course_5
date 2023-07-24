CREATE DATABASE course_5;

--Общая таблица со всеми (почти) данными запроса
CREATE TABLE vacancies(
	vacancy_id int PRIMARY KEY,
	company varchar(100) NOT NULL,
	vacancy varchar(100) NOT NULL,
	url text,
	city varchar(100) NOT NULL,
	salary_min int,
	salary_max int
);

--Таблица с названиями компаний и числом вакансий для каждой компании
CREATE TABLE company_vacancies_count(
	company varchar(100) NOT NULL,
	amount_of_vacancies int
);

--Таблица со средними значениями зарплат
CREATE TABLE average_salary(
	company varchar(100) NOT NULL,
	avg_salary int
);

--Таблица с вакансиями, зарплата которых выше средней
CREATE TABLE higher_salary(
	vacancy_id int PRIMARY KEY,
	vacancy varchar(100) NOT NULL,
	company varchar(100) NOT NULL,
	url text,
	salary_min int
);

--Таблица с вакансиями, отобранными по ключевому слову
CREATE TABLE vacancies_with_keyword(
	vacancy_id int PRIMARY KEY,
	vacancy varchar(100) NOT NULL,
	company varchar(100) NOT NULL,
	url text,
	salary_min int
);

--Short-версия таблицы со всеми вакансиями
CREATE TABLE vacancies_short(
	vacancy varchar(100) NOT NULL,
	company varchar(100) NOT NULL,
	url text,
	salary_min int
)

--Запросы для просмотра результатов в pgAdmin
SELECT * FROM vacancies_short
SELECT * FROM company_vacancies_count
SELECT * FROM average_salary
SELECT * FROM higher_salary
SELECT * FROM vacancies_with_keyword
