from flask import Flask, render_template, request
from class_hh import Parser_HH

app = Flask(__name__)


@app.route("/")
def index():
    #
    main_data = {
        'a': 'A',
        'b': 'B',
        'c': 'C'
    }

    context = {
        'name': 'Ильдар Шайдуллин',
        'mail': "ildarets@mail.ru",
        'phone' : 89600990747
    }

    # return render_template('index.html', main_data=main_data, **context)
    return render_template('index.html', main_data=main_data, name='Leo', age=99)


@app.route('/contacts/')
def contacts():
    # где то взяли данные
    developer_name = 'Ильдар Шайдуллин'
    # Контекст name=developer_name - те данные, которые мы передаем из view в шаблон
    # context = {'name': developer_name}
    # Словарь контекста context
    # return render_template('contacts.html', context=context)
    return render_template('contacts.html', name=developer_name, creation_date='16.01.2020')


# @app.route('/results/', methods=['GET'])
# def results():
#
#     return render_template('forma.html', text = 'Перед просмотром результатов сначала заполните форму')
#


@app.route('/run/', methods=['GET'])
def run_get():
    # with open('main.txt', 'r') as f:
    #     text = f.read()
    return render_template('forma.html', text = 'Заполните форму')
    # with open('main.txt', 'a') as f:
    #     f.write('hello')


@app.route('/run/', methods=['POST'])
def run_post():
    # Как получть данные формы
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