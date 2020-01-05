import requests
import pprint

DOMAIN = 'https://api.hh.ru/'

url_vacancies = f'{DOMAIN}vacancies'

params = {
    'text': 'C# developer',
    # страница
    'page': 1
}

result = requests.get(url_vacancies, params=params).json()

pprint.pprint(result)

salary = result['items'][0]['salary']['to']
print(salary)
sal = []
for i in range(20):
    if result['items'][i]['salary'] == None:
        continue
    else:
        salary = result['items'][i]['salary']['to']
        sal.append(salary)
print(sal)
#
# items = result['items']
#
# first = items[0]
#
# print(len(items))
#
# pprint.pprint(first)
#
# print(first['alternate_url'])
# one_vacancy_url = first['url']
#
# result = requests.get(one_vacancy_url, params=params).json()
#
# pprint.pprint(result)

# params = {
#     'text': 'NAME:(Python OR Java) AND COMPANY_NAME:(1 OR 2 OR Yandex) AND (Django OR Spring)',
#     # страница
#     'page': 1
# }
#
# result = requests.get(url_vacancies, params=params).json()
#
# pprint.pprint(result)