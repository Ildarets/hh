import time
import requests
import statistics


class Parser_HH:
    def __init__(self, QUESTIONS, CITY):
        self.QUESTIONS = QUESTIONS
        self.CITY = CITY

    def vacansis_found(self):
        ''' Найдено вакансий'''
        url = 'https://api.hh.ru/vacancies'
        params = {'text': f'NAME:({self.QUESTIONS}) AND {self.CITY}'}
        result = requests.get(url, params=params).json()
        found = result['found']
        return found

    def list_salary_mean(self):
        '''Средняя зарплата'''
        url = 'https://api.hh.ru/vacancies'
        list_salary = []
        for i in range(100):
            params = {
                'text': f'NAME:({self.QUESTIONS}) AND {self.CITY}',
                'page': i
            }

            result = requests.get(url, params=params).json()
            items = result['items']

            for item in items:
                result = requests.get(item['url']).json()

                # Вычисляем среднюю зарплату
                if item['salary'] is not None:
                    salary = item['salary']['from']
                    list_salary.append(salary)
                    salary = item['salary']['to']
                    list_salary.append(salary)

        list_salary_to = []
        for i in list_salary:
            if i != None:
                list_salary_to.append(i)

        list_salary_mean = statistics.mean(list_salary_to)
        # Обработка ошибки при неправильно введенном запросе где будут нули
        try:
            list_salary_mean = round(list_salary_mean)
        except:
            list_salary_mean = 0

        return list_salary_mean

    def key_skills(self):
        """Список ключевых навыков"""
        key_skills = {}
        url = 'https://api.hh.ru/vacancies'
        key_skills_list = []

        # Охватываем максимальное число страниц
        for i in range(100):
            params = {
                'text': f'NAME:({self.QUESTIONS}) AND {self.CITY}',
                'page': i
            }

            result = requests.get(url, params=params).json()
            items = result['items']

            for item in items:
                result = requests.get(item['url']).json()

                # Вычисляем навыки
                for res in result['key_skills']:
                    key_skills_list.append(res['name'])
                time.sleep(0.1)

        for skill in key_skills_list:
            if skill in key_skills:
                key_skills[skill] += 1
            else:
                key_skills[skill] = 1

        result_vac = sorted(key_skills.items(), key = lambda x: x[1], reverse= True)

        return result_vac