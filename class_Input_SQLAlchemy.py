from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from class_hh_sql import Parser_HH


class Input_SQLAlchemy:
    """Инициализируем объект класса для работы с запросом клиента"""

    def __init__(self, QUESTIONS, CITY):
        self.QUESTIONS = QUESTIONS
        self.CITY = CITY
        parser = Parser_HH(QUESTIONS, CITY)
        self.skills_list = parser.key_skills()
        # print(skills_list)

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

        engine = create_engine('sqlite:///orm.sqlite', echo=False)
        # Заполняем таблицы
        Session = sessionmaker(bind=engine)

        # create a Session
        session = Session()

        """ ДЕлаем объект и заполняем таблицу должностью, городом и навыками"""

        # Список ключевых навыков
        key_skills_list = self.skills_list

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
        name_key_skills_list = []

        for key in key_skills_list:
            # Делаем запрос по имени навыка
            key_query = session.query(self.Skill).filter(self.Skill.name == key).first()
            key_query_id = key_query.name
            name_key_skills_list.append(key_query_id)

        # Узанем id  вакансии
        vacancy_query = session.query(self.Vacancy).filter(self.Vacancy.name == self.QUESTIONS).first()
        vacancy_id = vacancy_query.id

        # Заполняем таблицу vacancy key_skills. Заполняем id  вакансии и id ключеваго навыка
        for skill_name in name_key_skills_list:
            skill_query_val = session.query(self.Skill).filter(self.Skill.name == skill_name).first()
            if not skill_query_val:
                key_query = session.query(self.Skill).filter(self.Skill.name == skill_name).first()
                key_query_id = key_query.id
                vac_sk = self.Vacancyskill.insert().values(vacancy_id=vacancy_id, skill_id=key_query_id)
                session.execute(vac_sk)

        session.commit()

    def select_table_sql(self, question, city):

        engine = create_engine('sqlite:///orm.sqlite', echo=False)
        # Заполняем таблицы
        Session = sessionmaker(bind=engine)

        # create a Session
        session = Session()

        city_query = session.query(self.Region).filter(self.Region.name == city).first()

        vacancies = session.query(self.Vacancy).filter(self.Vacancy.region_id == city_query.id).all()
        vacancies_query = session.query(self.Vacancy).filter(self.Vacancy.name == question).first()

        key_skills_list = session.query(self.Vacancyskill).filter(
            self.Vacancyskill.c.vacancy_id == vacancies_query.id).all()

        return_key_skills_list_id = []
        for key in key_skills_list:
            key_skill = key[0]
            return_key_skills_list_id.append(key_skill)

        skills_list = []
        for skill_id in return_key_skills_list_id:
            skill_real = session.query(self.Skill).filter(self.Skill.id == skill_id).first()
            skills_list.append(skill_real.name)


        return skills_list
