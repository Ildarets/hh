from flask import Flask, render_template, request
from class_hh import Parser_HH

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


if __name__ == "__main__":
    app.run(debug=True)