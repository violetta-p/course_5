import requests


class HeadHunterAPI:
    def __init__(self, employer):
        self.employer = employer

    def get_employer_id(self):
        params = {
            'text': self.employer,
            'only_with_vacancies': True,
            'page': 0,
            'per_page': 3
        }
        try:
            all_emp_id = []
            response = requests.get('https://api.hh.ru/employers', params=params)
            if response.status_code == 200:
                employer_id = response.json()["items"]
                for i in range(len(employer_id)-1):
                    all_emp_id.append(employer_id[i]["id"])
                return all_emp_id
            else:
                print(f'HeadHunter response: Error {response.status_code}')
                return None

        except (requests.exceptions.HTTPError, requests.ConnectionError):
            print('HeadHunter response: Connection failed')
            return None

    @staticmethod
    def get_vacancies(employer_id, count_page=5):
        params = {
            'employer_id': employer_id,  # Ключевое слово запроса
            'page': 0,  # Индекс страницы поиска на HH
            'per_page': 10  # Кол-во вакансий на 1 странице
        }
        data = []
        try:
            while params["page"] < count_page:
                response = requests.get('https://api.hh.ru/vacancies', params=params)
                if response.status_code == 200:
                    print(f"Парсинг {params['page'] + 1} страницы")
                    data.extend(response.json()["items"])
                    params["page"] += 1
                else:
                    print(f'HeadHunter response: Error {response.status_code}')
                    return None
            return data
        except (requests.exceptions.HTTPError, requests.ConnectionError):
            print('HeadHunter response: Connection failed')
            return None
