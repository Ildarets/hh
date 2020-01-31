import sqlite3
from class_hh_sql import Parser_HH

QUESTIONS = input("Какая должность? ")
CITY = input("Какой город? ")

skills_list = Parser_HH(QUESTIONS, CITY)

key_skills_list = skills_list.key_skills()

# Подключение к базе данных
conn = sqlite3.connect('hh.sqlite')

# Создаем курсор
cursor = conn.cursor()



cursor.execute('SELECT id from region where name = ?', (CITY,))
city = cursor.fetchall()
city = city[0][0]
# print(city)
try:
    cursor.execute('insert into vacancy(name, region_id) values(?, ?)', (QUESTIONS, city))
except:
    pass

cursor.execute('SELECT * from vacancy')
result = cursor.fetchall()
print(result)



try:
    cursor.execute('insert into region(name) values (?)', (CITY,))
except:
    pass

for key_skill in key_skills_list:
    try:
        cursor.execute('insert into key_skills(name) values (?)', (key_skill,))
    except:
        continue



cursor.execute('SELECT name from key_skills')
x_list = cursor.fetchall()
id_key_skills_list = []
for key in key_skills_list:

        cursor.execute('SELECT id from key_skills where name = ?', (key,))
        id_key_skills = cursor.fetchall()
        id_key_skills = id_key_skills[0][0]
        id_key_skills_list.append(id_key_skills)

cursor.execute('SELECT id from vacancy where name = ?', (QUESTIONS,))
vacancy_id = cursor.fetchall()
vacancy_id = vacancy_id[0][0]


result = cursor.fetchall()
for id in id_key_skills_list:

        cursor.execute('insert into vacancy_key_skills(vacancy_id, key_skills_id) values (?,?)', (vacancy_id, id))

cursor.execute('SELECT * from vacancy_key_skills')
result = cursor.fetchall()
print(result)



# # conn.commit()


#
# # Если запрос ничего не возращает то делаем execute
# cursor.execute("insert into vacancy_key_skills (vacancy_id, key_skills_id) VALUES (?, ?)", (1, 5))
#

#
# print(x)
#
#
#
#


# cursor.execute('SELECT * from region')
#
# result = cursor.fetchall()
# print(result)
#
# for item in result:
#     print(item)
#     print(type(item))
#
# cursor.execute('SELECT * from region where name=?', ('Москва',))
#
# print(cursor.fetchall())


# query = 'select vk.id, v.name, k.name from vacancy v, key_skills k, ' \
#         'vacancy_key_skills vk where vk.vacancy_id == v.id and' \
# #         ' vk.key_skills_id == k.id'
# query = 'select vk.id, v.name, k.name, r.name from vacancy v, ' \
#         'key_skills k, vacancy_key_skills vk, region r where vk.vacancy_id = v.id' \
#         ' and vk.key_skills_id = k.id and v.region_id = r.id'
# #
# # # Вывести в нормальном виде таблицу скилы + вакансии
# cursor.execute(query)
#
# print(cursor.fetchall())
#
