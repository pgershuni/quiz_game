import requests
from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from login import LoginForm
from registration import RegForm

app = Flask('app')
app.config['SECRET_KEY'] = 'secretkeyandexlyceum'


# Доделать:
# - Обычный личный кабинет со статистикой (Добавить в бд дополнительные колонки со статистикой )
# - Создание теста
# - Поиск
# - Способы сортировки на главной странице
# - Открытие тестов

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    user = requests.get(f'http://127.0.0.1:8080/api/users/{user_id}').json()['user']
    return User(user)


class User(UserMixin):

    def __init__(self, data):
        self._id = data['id']
        self._data = data

    def get_id(self):
        return self._id

    def get_data(self):
        return self._data



@app.route('/')
def start():
    return redirect('/login')


@app.route('/check_data/<_type>', methods=['GET', 'POST'])
def check_data(_type):


    req_data = requests.get('http://127.0.0.1:8080/api/users').json()['users']
    user = list(filter(lambda x: x['name'] == request.form['username'], req_data))

    print(req_data)

    if _type == 'login':
        if not user:
            error = 'неверный логин или пароль'

        elif user[0]['password'] == request.form['password']:
            login_user(User(user[0]))
            return redirect('/welcome')

        else:
            error = 'неверный логин или пароль'

        return render_template('login.html', form=LoginForm(), _error=error)

    else:
        if user:
            error = 'пользователь уже зарегистрирован'

        else:
            user_id = requests.post('http://127.0.0.1:8080/api/users', json={'name': request.form['username'],
                                                                   'about': '-',
                                                                   'login': request.form['login'],
                                                                   'password': request.form['password']
                                                                   }).json()
            user = requests.get(f'http://127.0.0.1:8080/api/users/{user_id}')['user']
            login_user(User(user))
            return redirect('/welcome')

        return render_template('reg.html', form=RegForm(), _error=error)


# Регистрация
@app.route('/registration', methods=['GET', 'POST'])
def reg():
    print('registration')

    form = RegForm()

    if form.validate_on_submit():
        pass

    return render_template('reg.html', form=form)


# Страница авторизации
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    return render_template('login.html', form=form)


# Приветствующая страница с рекомендованными (рандомными, ну или выбраны, допустим, по самому высокому рейтингу) тестами
@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    req_data = requests.get('http://127.0.0.1:8080/api/tests').json()['tests']
    tests = []
    for test in req_data:
        tests.append({'title': test['title'], 'description': test['about'], 'questions': len(test['questions']),
                      'date': '01.01.02'})

    print('success authorization')

    return render_template('welcome.html', lst=tests, username=current_user.get_data()['name'])


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
@app.route('/profile/stats', methods=['GET', 'POST'])
def stats():
    print("stats")

    data = requests.get('http://127.0.0.1:8080/api/users').json()
    print(data)

    return render_template('stats.html')


# Создание тестов
@app.route('/creating/<_next>', methods=['GET', 'POST'])
def create(_next):
    print("creating")

    if _next == "questions":
        return render_template("creating_question.html")

    else:
        return render_template('creating.html')


if __name__ == '__main__':
    app.run(debug=True)
