from flask import Flask, render_template, request
from class_hh import Parser_HH
from main_sql import Input_SQL
from class_Input_SQLAlchemy import Input_SQLAlchemy
app = Flask(__name__)


@app.route("/")
def index():
    # Возвращаем главную страницу

    return render_template('index.html', name='МегаПарсер')


@app.route('/contacts/')
def contacts():
    """ЗАполняем страницу контактов"""
    context = {
        'name': 'Ильдар Шайдуллин',
        'mail': "ildarets@mail.ru",
        'phone' : +79600990747,
        'phone_neiron' : '8(495) 223-32-22'
    }
    return render_template('contacts.html', context = context)


@app.route('/run/', methods=['GET'])
def run_get():
    text = 'Заполните форму ниже. Укажите должность и город!'
    return render_template('forma.html', text = text)


@app.route('/run/', methods=['POST'])
def run_post():
    """Запросы в парсер по должности и городу"""
    QUESTIONS = request.form['QUESTIONS']
    CITY = request.form['CITY']
    vacancy = Parser_HH(QUESTIONS, CITY)

    return render_template('results.html',
                           vacancy = vacancy.vacansis_found(),
                           list_salary_mean = vacancy.list_salary_mean(),
                           CITY = CITY,
                           QUESTIONS = QUESTIONS,
                           key_skills = vacancy.key_skills()
                           )

# Для работы с SQL
@app.route('/runSQL/', methods=['GET'])
def run_getSQL():
    text = 'Заполните форму ниже. Укажите должность и город!'
    return render_template('formaSQL.html', text = text)


@app.route('/runSQL/', methods=['POST'])
def run_postSQL():
    """Запросы в парсер по должности и городу"""
    QUESTIONS = request.form['QUESTIONS']
    CITY = request.form['CITY']
    input_table = Input_SQL(QUESTIONS, CITY)

    output_table = input_table.select_table_sql(QUESTIONS, CITY)

    """Если запрос возвращает пустой список, то тогда парсим данные и возвращаем список ключевых навыков"""
    if output_table == []:
        input_table.full_table_sql()
        output_table = input_table.select_table_sql(QUESTIONS, CITY)

    return render_template('resultsSQL.html',
                           CITY = CITY,
                           QUESTIONS = QUESTIONS,
                           key_skills = output_table
                           )


# Для работы с SQLAlchemy
@app.route('/runSQLAlchemy/', methods=['GET'])
def run_getSQLAlchemy():
    text = 'Заполните форму ниже. Укажите должность и город!'
    return render_template('formaSQLAlchemy.html', text = text)


@app.route('/runSQLAlchemy/', methods=['POST'])
def run_postSQLAlchemy():
    """Запросы в парсер по должности и городу"""
    QUESTIONS = request.form['QUESTIONS']
    CITY = request.form['CITY']
    input_table = Input_SQLAlchemy(QUESTIONS, CITY)
    input_table.create_table()
    output_table = input_table.select_city_question(QUESTIONS, CITY)
    print(output_table)
    """Если запрос возвращает пустой список, то тогда парсим данные и возвращаем список ключевых навыков"""
    if not output_table:

        input_table.full_table_sql(QUESTIONS, CITY)
        output_ = input_table.select_table_sql(QUESTIONS, CITY)
    else:
        output_ = input_table.select_table_sql(QUESTIONS, CITY)

    return render_template('resultsSQLAlchemy.html',
                           CITY = CITY,
                           QUESTIONS = QUESTIONS,
                           key_skills = output_
                           )


# select v.name as vacancy_name, k.name as key_skills_name from vacancy v , key_skills k, vacancy_key_skills vk, region r where vk.vacancy_id == v.id and vk.key_skills_id == k.id and v.name == 'R' and r.name = 'Тула'
if __name__ == "__main__":
    app.run(debug=True)