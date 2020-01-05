import time
import requests
import pprint
import statistics

QUESTIONS = str(input("Какая должность Вас интересует???  "))
CITY = str(input("Какой регион???  "))

key_skills = {}
url = 'https://api.hh.ru/vacancies'
key_skills_list = []
list_salary = []

params = {'text': f'NAME:({QUESTIONS}) AND {CITY}'}
result = requests.get(url, params=params).json()
found = result['found']


for i in range(100): # Охватываем максимальное число страниц
    params = {
        'text': f'NAME:({QUESTIONS}) AND {CITY}',
        'page': i
    }

    result = requests.get(url, params=params).json()
    items = result['items']
    found = result['found']

    for item in items:
        result = requests.get(item['url']).json()

        # Вычисляем среднюю зарплату
        if item['salary'] is not None:
            salary = item['salary']['from']
            list_salary.append(salary)
            salary = item['salary']['to']
            list_salary.append(salary)

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

list_salary_to = []
for i in list_salary:
    if i != None:
        list_salary_to.append(i)


list_salary_mean = statistics.mean(list_salary_to)

print(f'Найдено {found}  вакансий')
print(f'Средняя зарплата  {list_salary_mean} рублей!')

for i in result_vac:
    print(*i)

