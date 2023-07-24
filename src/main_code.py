from src.vacancies_collector import HeadHunterAPI
from src.data_preparation import PreparedData
from src.DB_module import SaveToDataBase, DataCleaner, DBManager


def get_data(keyword: str):
    """
    Получение данных по ключевому слову с различных ресурсов
    и приведение их к единому формату:

    {  "profession": '', "url": '', "city": '',
       "company": '', "schedule": '',
       "experience": '', "salary_min": '',
       "salary_max": ''}

    """
    hh_api = HeadHunterAPI(keyword)
    hh_ids = hh_api.get_employer_id()
    for i in range(len(hh_ids)):
        hh_vacancies = hh_api.get_vacancies(hh_ids[i])
        data_prep = PreparedData(hh_vacancies)
        data_prep.get_prepared_data_hh()
    return PreparedData.all_data


def user_interface():
    print("------------------------------------------------------------------------")
    print("Выберите действие:")
    print("------------------------------------------------------------------------")
    print("1 - Получить список всех вакансий")
    print("2 - Получить список компаний и количество вакансий у каждой компании")
    print("3 - Получает среднюю зарплату по вакансиям каждой компании")
    print("4 - Получить список вакансий с зарплатой выше средней по всем вакансиям")
    print("5 - Получить список вакансий по ключевому слову")
    print("6 - Выход")
    print("------------------------------------------------------------------------")


def execute_bd_manager(user_choice):
    bd_manager = DBManager()

    if user_choice == "1":
        bd_manager_response = bd_manager.get_all_vacancies()
        print(bd_manager_response)
    if user_choice == "2":
        bd_manager_response = bd_manager.get_companies_and_vacancies_count()
        print(bd_manager_response)
    if user_choice == "3":
        bd_manager_response = bd_manager.get_avg_salary()
        print(bd_manager_response)
    if user_choice == "4":
        bd_manager_response = bd_manager.get_vacancies_with_higher_salary()
        print(bd_manager_response)
    if user_choice == "5":
        user_keyword = input("Введите слово для поиска: ").lower()
        bd_manager_response = bd_manager.get_vacancies_with_keyword(user_keyword)
        print(bd_manager_response)


def main_part():
    """
    Основная часть программы. Собирает все классы и функции
    """
    # platforms = ["HeadHunter"]

    user_answer = input("Очистить результаты предыдущих запросов?: [yes/no]")
    if user_answer.lower() in ("yes", "да"):
        clean_data = DataCleaner()
        clean_data.delete_all_data()

    continue_searching = "yes"

    while continue_searching.lower() in ("yes", "да"):
        print("\nВозможные варианты: 2ГИС, Яндекс, СБЕР, Тинькофф, Tele2, МТС, ВТБ, Сибур, VK, Газпром нефть\n")

        user_keyword = input("Введите интересующего вас работодателя: ")
        keyword = user_keyword if user_keyword != "" else '2ГИС'

        vacancies_data = get_data(keyword)
        db_saver = SaveToDataBase(vacancies_data)
        db_saver.write_data()

        continue_searching = input("Выбрать другого работодателя?: [yes/no]")

    user_interface()
    user_choice = input(": ")
    while user_choice != "6":
        execute_bd_manager(user_choice)
        user_interface()
        user_choice = input(": ")


if __name__ == "__main__":
    main_part()
