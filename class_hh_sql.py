import time
import requests
import statistics


class Parser_HH:
    def __init__(self, QUESTIONS, CITY):
        self.QUESTIONS = QUESTIONS
        self.CITY = CITY

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

        result_vac = sorted(key_skills.items(), key=lambda x: x[1], reverse=True)

        key_list = []
        for key_skill in result_vac[:20]:
            key_list.append(key_skill[0])

        return key_list
