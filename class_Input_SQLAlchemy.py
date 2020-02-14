from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from class_hh_sql import Parser_HH


class Input_SQLAlchemy:
    """Инициализируем объект класса для работы с запросом клиента"""

    def __init__(self, QUESTIONS, CITY):
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

            def __init__(self, name):
                self.name = name

            def __str__(self):
                return f'{self.id}) {self.name}'

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
        parser = Parser_HH(self.QUESTIONS, self.CITY)
        skills_list = parser.key_skills()
        engine = create_engine('sqlite:///orm.sqlite', echo=False)
        # Заполняем таблицы
        Session = sessionmaker(bind=engine)

        # create a Session
        session = Session()

        """ ДЕлаем объект и заполняем таблицу должностью, городом и навыками"""

        # Список ключевых навыков
        key_skills_list = skills_list

        # Делаем запрос по имени города
        city = session.query(self.Region).filter(self.Region.name == self.CITY).first()
        # Если этого города нет то мы его добавляем
        if not city:
            session.add(self.Region(self.CITY))
        session.commit()
        # Делаем запрос по имени города
        city = session.query(self.Region).filter(self.Region.name == self.CITY).first()
        # ищем id города
        city_id = city.id

        # Заполняем вакансии
        # Делаем запрос по имени города
        vacancy = session.query(self.Vacancy).filter(self.Vacancy.name == self.QUESTIONS).first()
        # Если этой вакансии нет то мы ее добавляем
        if not vacancy:
            session.add(self.Vacancy(self.QUESTIONS, city_id))
        session.commit()
        # Заполняем навыки
        for skill in key_skills_list:
            # Делаем запрос по имени навыка
            skill_query = session.query(self.Skill).filter(self.Skill.name == skill).first()
            # Если этой навыка нет то мы его добавляем
            if not skill_query:
                session.add(self.Skill(skill))
            session.commit()

        # Делаем список из id ключевых навыков
        id_key_skills_list = []

        for key in key_skills_list:
            # Делаем запрос по имени навыка
            key_query = session.query(self.Skill).filter(self.Skill.name == key).first()
            key_query_id = key_query.id
            id_key_skills_list.append(key_query_id)

        # Узанем id  вакансии
        vacancy_query = session.query(self.Vacancy).filter(self.Vacancy.name == self.QUESTIONS).first()
        vacancy_id = vacancy_query.id

        # Заполняем таблицу vacancy key_skills. Заполняем id  вакансии и id ключеваго навыка
        for id_skill in id_key_skills_list:
            key_skills_list = session.query(self.Vacancyskill).filter(self.Vacancyskill.c.vacancy_id == vacancy_id).filter(self.Vacancyskill.c.skill_id == id_skill).all()
            if key_skills_list == []:
                vac_sk = self.Vacancyskill.insert().values(vacancy_id=vacancy_id, skill_id=id_skill)
                session.execute(vac_sk)

            session.commit()

    def select_city_question(self, city, question):
        engine = create_engine('sqlite:///orm.sqlite', echo=False)
        # Заполняем таблицы
        Session = sessionmaker(bind=engine)

        # create a Session
        session = Session()
        # Делаем запрос по имени города
        region = session.query(self.Region).filter(self.Region.name == city).first()
        # Получаем объект вакансии для получения id
        if not region:
            return region
        vacancies_query = session.query(self.Vacancy).filter(self.Vacancy.region_id == region.id).filter(self.Vacancy.name == question).first()

        #  добавляем
        session.add(self.Vacancy(question, city))
        session.commit()

        return vacancies_query



    def select_table_sql(self, question, city):
        skills_list = []
        engine = create_engine('sqlite:///orm.sqlite', echo=False)
        # Заполняем таблицы
        Session = sessionmaker(bind=engine)

        # create a Session
        session = Session()
        # Получаем объект вакансии для получения id
        vacancies_query = session.query(self.Vacancy).filter(self.Vacancy.name == question).first()
        # Если список пустой то, возвращаем надпись что ничего нет по данной вакансии
        if not vacancies_query:
            skills_list = []
            return skills_list

        # Получаем кортеж из таблицы Vacancyskill где приссутствуют ключевые навыки для этой вакансии
        key_skills_list = session.query(self.Vacancyskill).filter(
            self.Vacancyskill.c.vacancy_id == vacancies_query.id).all()


        # Получаем список id для поиска ключевых навыков из таблицы Skill
        return_key_skills_list_id = []
        for key in key_skills_list:
            key_skill = key[2]
            return_key_skills_list_id.append(key_skill)

        # Получаем список навыков по id из таблицы Skill

        for skill_id in return_key_skills_list_id:
            skill_real = session.query(self.Skill).filter(self.Skill.id == skill_id).first()
            skills_list.append(skill_real.name)


        return skills_list
