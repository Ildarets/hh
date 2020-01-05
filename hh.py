import time
import requests
import pprint

QUESTIONS = str(input("Какая должность Вас интересует???  "))
CITY = str(input("Какой регион???  "))

key_skills = {}
url = 'https://api.hh.ru/vacancies'
key_skills_list = []
for i in range(100):
    params = {
        'text': f'NAME:({QUESTIONS}) AND {CITY}',
        'page': i
    }

    result = requests.get(url, params=params).json()
    items = result['items']

    for item in items:
        result = requests.get(item['url'], params=params).json()
        for res in result['key_skills']:
            key_skills_list.append(res['name'])
        time.sleep(0.1)

for skill in key_skills_list:
    if skill in key_skills:
        key_skills[skill] += 1
    else:
        key_skills[skill] = 1

result_vac = sorted(key_skills.items(), key = lambda x: x[1], reverse= True)
pprint.pprint(result_vac)


