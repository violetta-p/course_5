class PreparedData:
    """
    Класс предназначен для приведения данных
    единому формату и сохранения данных в единый список.
    """

    all_data = []
    items = ("null", [], {}, "", False, "None", None, "NoneType")

    def __init__(self, hh_data):
        self.hh_data = hh_data

    def get_prepared_data_hh(self):
        if self.hh_data is None:
            return None
        vacancies = self.hh_data
        for vacancy in vacancies:
            area = vacancy.get("area", {}).get("name")
            salary_min = 0 if vacancy.get("salary", {}) in PreparedData.items or type(vacancy.get("salary", {})) == 'NoneType' else vacancy["salary"]["from"]
            salary_max = 0 if vacancy.get("salary", {}) in PreparedData.items or type(vacancy.get("salary", {})) == 'NoneType' else vacancy["salary"]["to"]
            salary = self.convert_salary_from_str_to_int(salary_min, salary_max)
            name = vacancy.get("name", "-")
            vacancy_url = vacancy.get("alternate_url")
            vacancy_id = vacancy.get("id")
            company_name = "-" if vacancy.get("employer", {}) in PreparedData.items else vacancy["employer"]["name"]

            vac_info = {
                "vacancy_id": vacancy_id, "company": company_name,
                "profession": name, "url": vacancy_url, "city": area,
                "salary_min": salary[0], "salary_max": salary[1],
            }
            PreparedData.all_data.append(vac_info)

    @staticmethod
    def convert_salary_from_str_to_int(s_min, s_max):
        salary_min = 0 if type(s_min) == "NoneType" or s_min in PreparedData.items else int(s_min)
        salary_max = 0 if type(s_max) == "NoneType" or s_max in PreparedData.items else int(s_max)

        if salary_min != 0 and salary_max == 0:
            salary_max = salary_min
        elif salary_min == 0 and salary_max != 0:
            salary_min = salary_max

        return [salary_min, salary_max]
