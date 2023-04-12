from flask import Flask, render_template, redirect, request
from login import LoginForm
from registration import RegForm

app = Flask('app')
app.config['SECRET_KEY'] = 'secretkeyandexlyceum'


# Доделать:
# - Проверка введенных данных при регистрации (перекидывание на определенную ссылку, где будет происходить проверка)
# - Обычный личный кабинет со статистикой
# - Создание теста
# - Поиск
# - Способы сортировки на главной странице
# - Открытие тестов
# - Рекоммендации

@app.route('/')
def start():
    return redirect('/login')


# Регистрация
@app.route('/registration', methods=['GET', 'POST'])
def reg():
    print('registration')

    form = RegForm()

    if form.validate_on_submit():
        print('redirection')
        return redirect('/welcome')

    return render_template('reg.html', form=form)


# Страница авторизации
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        print('redirection')
        return redirect('/welcome')

    return render_template('login.html', form=form)


# Приветствующая страница с рекомендованными (рандомными, ну или выбраны, допустим, по самому высокому рейтингу) тестами
@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    global data

    lst = [{"title": "Первый тест", "description": "Биология", "questions": 3, "date": "29.02.1999"},
           {"title": 'Второй тест', "description": "Математика", "questions": 5, "date": "01.01.2021"},
           {"title": 'Третий тест', "description": "Кулинария", "questions": 10, "date": "02.03.2023"}]

    try:
        params = {
            'username': request.form['username'],
            'password': request.form['password'],
            'lst': lst
        }

        print('success authorization')

        data = params

        return render_template('welcome.html', **params)

    except KeyError:
        print('already in system')

        return render_template('welcome.html', **data)


# Главная страница со всеми тестами
@app.route('/main', methods=['GET', 'POST'])
def main():
    params = {
        "list_of_tests": [{"title": "Первый тест", "description": "Биология", "questions": 3, "date": "29.02.1999"},
                          {"title": 'Второй тест', "description": "Математика", "questions": 5, "date": "01.01.2021"},
                          {"title": 'Третий тест', "description": "Кулинария", "questions": 10, "date": "02.03.2023"}]
    }

    print("main page opened")

    return render_template("main.html", **params)


# Открывается при нажатии на кнопку "Найти"
@app.route('/search', methods=['GET', 'POST'])
def find():
    print("searching")

    return render_template('searching.html')


# Личный кабинет
@app.route('/profile/<_next>', methods=['GET', 'POST'])
def cabinet(_next):
    print("profile")

    # Переадресация на мои тесты и на решенные тесты
    if _next in ("my_tests", "ready_tests"):
        return render_template('my_tests.html' if _next == "my_tests" else 'ready_tests.html')

    # Личная статистика
    elif _next == "per_acc":
        return render_template("per_acc.html")


# Создание тестов
@app.route('/creating', methods=['GET', 'POST'])
def create():
    print("creating")

    return render_template('creating.html')


# Страница с рекомендациями
@app.route('/recommendation', methods=['GET', 'POST'])
def recs():
    print('recommendations')

    return render_template('recommendations.html ')


if __name__ == '__main__':
    app.run(debug=True)
