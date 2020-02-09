from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from class_hh_sql import Parser_HH

class Input_SQLAlchemy:
    """Инициализируем объект класса для работы с запросом клиента"""
    def __init__(self,QUESTIONS, CITY):
        self.QUESTIONS = QUESTIONS
        self.CITY = CITY



    def create_table(self):
        engine = create_engine('sqlite:///orm.sqlite', echo=False)

        Base = declarative_base()

        Vacancyskill = Table('vacancyskill', Base.metadata,
                             Column('id', Integer, primary_key=True),
                             Column('vacancy_id', Integer, ForeignKey('vacancy.id')),
                             Column('skill_id', Integer, ForeignKey('skill.id'))
                             )

        class Skill(Base):
            __tablename__ = 'skill'
            id = Column(Integer, primary_key=True)
            name = Column(String, unique=True)

            def __init__(self, name):
                self.name = name

            def __str__(self):
                return self.name

        class Region(Base):
            __tablename__ = 'region'
            id = Column(Integer, primary_key=True)
            name = Column(String)
            number = Column(Integer, nullable=True)

            # note = Column(String, nullable=True)

            def __init__(self, name, number):
                self.name = name
                self.number = number

            def __str__(self):
                return f'{self.id}) {self.name}: {self.number}'

        class Vacancy(Base):
            __tablename__ = 'vacancy'
            id = Column(Integer, primary_key=True)
            name = Column(String)
            # Связь 1 - много, связь внешний ключ
            region_id = Column(Integer, ForeignKey('region.id'))

            def __init__(self, name, region_id):
                self.name = name
                self.region_id = region_id


        # Создание таблицы
        Base.metadata.create_all(engine)

        self.Skill = Skill
        self.Region = Region
        self.Vacancyskill = Vacancyskill
        self.Vacancy = Vacancy

    def full_table_sql(self):

        engine = create_engine('sqlite:///orm.sqlite', echo=False)
        # Заполняем таблицы
        Session = sessionmaker(bind=engine)

        # create a Session
        session = Session()

        """ ДЕлаем объект и заполняем таблицу должностью, городом и навыками"""
        skills_list = Parser_HH(self.QUESTIONS, self.CITY)
        # Список ключевых навыков
        key_skills_list = skills_list.key_skills()

        #Делаем запрос по имени города
        city = session.query(self.Region).filter(self.Region.name == self.CITY).first()

        # ищем id города
        city_id = city.id

        # Если этого города нет то мы его добавляем
        if not city_id:
            count_id = session.query(self.Region).filter(self.Region.name == self.CITY).count()
            session.add([self.Region(self.CITY, count_id + 1)])
        session.commit()

        # Делаем запрос по имени города
        city = session.query(self.Region).filter(self.Region.name == self.CITY).first()

        # ищем id города
        city_id = city.id






        # Заполняем вакансии
        # Делаем запрос по имени города
        vacancy = session.query(self.Vacancy).filter(self.Vacancy.name == self.QUESTIONS).first()
        # ищем id вакансии
        vacancy_id = vacancy.id
        # Если этой вакансии нет то мы ее добавляем
        if not vacancy_id:
            count_id = session.query(self.Vacancy).filter(self.Vacancy.name == self.QUESTIONS).count()
            session.add([self.Vacancy(self.QUESTIONS, city_id)])
        session.commit()
        # Делаем запрос по имени города
        vacancy = session.query(self.Vacancy).filter(self.Vacancy.name == self.QUESTIONS).first()
        # ищем id вакансии
        vacancy_id = vacancy.id



        # cursor.execute('SELECT id from region where name = ?', (self.CITY,))
        # city = cursor.fetchall()
        # city = city[0][0]
        # # Заполняем вакансии
        # try:
        #     cursor.execute('insert into vacancy(name, region_id) values(?, ?)', (self.QUESTIONS, city))
        # except:
        #     pass

        # Заполняем ключевые навыки из списка полученного от класса Parser_HH
        for key_skill in key_skills_list:
            # Делаем запрос по имени города
            skill = session.query(self.Skill).filter(self.Skill.name == key_skill).first()
            # ищем id вакансии
            skill_id = skill.id
            # Если этой вакансии нет то мы ее добавляем
            if not skill_id:
                count_id = session.query(self.Skill).filter(self.Skill.name == key_skill).count()
                session.add([self.Skill(key_skill)])
            session.commit()
            # Делаем запрос по имени города
            skill = session.query(self.Skill).filter(self.Skill.name == key_skill).first()
            # ищем id вакансии
            skill_id = skill.id


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
