import sqlite3
from class_hh_sql import Parser_HH

# QUESTIONS = input("Какая должность? ")
# CITY = input("Какой город? ")

class Input_SQL:
    """Инициализируем объект класса для работы с запросом клиента"""
    def __init__(self,QUESTIONS, CITY):
        self.QUESTIONS = QUESTIONS
        self.CITY = CITY


    def full_table_sql(self):
        """ ДЕлаем объект и заполняем таблицу должностью, городом и навыками"""
        skills_list = Parser_HH(self.QUESTIONS, self.CITY)
        # Список ключевых навыков
        key_skills_list = skills_list.key_skills()

        # Подключение к базе данных
        conn = sqlite3.connect('hh.sqlite', check_same_thread=False)

        # Создаем курсор
        cursor = conn.cursor()

        # Заполняем город
        try:
            cursor.execute('insert into region(name) values (?)', (self.CITY,))
        except:
            pass

        # Заполняем вакансии, для этого надо сначала узнать id города
        cursor.execute('SELECT id from region where name = ?', (self.CITY,))
        city = cursor.fetchall()
        city = city[0][0]
        # Заполняем вакансии
        try:
            cursor.execute('insert into vacancy(name, region_id) values(?, ?)', (self.QUESTIONS, city))
        except:
            pass

        # Заполняем ключевые навыки из списка полученного от класса Parser_HH
        for key_skill in key_skills_list:
            try:
                cursor.execute('insert into key_skills(name) values (?)', (key_skill,))
            except:
                continue



        # Делаем список из id ключевых навыков
        id_key_skills_list = []

        for key in key_skills_list:
                cursor.execute('SELECT id from key_skills where name = ?', (key,))
                id_key_skills = cursor.fetchall()
                id_key_skills = id_key_skills[0][0]
                id_key_skills_list.append(id_key_skills)

        #Узанем id  вакансии
        cursor.execute('SELECT id from vacancy where name = ?', (self.QUESTIONS,))
        vacancy_id = cursor.fetchall()
        vacancy_id = vacancy_id[0][0]

        # Заполняем таблицу vacancy key_skills. Заполняем id  вакансии и id ключеваго навыка
        for id in id_key_skills_list:
                cursor.execute('insert into vacancy_key_skills(vacancy_id, key_skills_id) values (?,?)', (vacancy_id, id))

        conn.commit()

    def select_table_sql(self, question, city):
        # Подключение к базе данных
        conn = sqlite3.connect('hh.sqlite', check_same_thread=False)

        # Создаем курсор
        cursor = conn.cursor()

        cursor.execute('select k.name from vacancy v , key_skills k, vacancy_key_skills vk, region r where vk.vacancy_id == v.id and vk.key_skills_id == k.id and v.name == ? and r.name = ?', (question,city ))
        key_skills_list = cursor.fetchall()

        return_key_skills_list = []
        for key in key_skills_list:
            key_skill = key[0]
            return_key_skills_list.append(key_skill)

        return return_key_skills_list

