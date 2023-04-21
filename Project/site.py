import requests
from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from forms import LoginForm, RegForm, Create, CreateType, CreateQuestion

app = Flask('app')
app.config['SECRET_KEY'] = 'secretkeyandexlyceum'

# Доделать:
# - Создание теста (динамическое использование)
# - Поиск по имени
# - Открытие тестов
# !!! - при создании теста количество вопросов должно сохраняться в каждой форме

# Заметки:
# - пока в creating-ах стоят затычки с nums

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    user = requests.get(f'http://127.0.0.1:8080/api/users/{user_id}').json()['user']
    print(user)
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
                                                                             }).json()['id']
            # print(user_id, requests.get(f'http://127.0.0.1:8080/api/users/{user_id}').json())
            user = requests.get(f'http://127.0.0.1:8080/api/users/{user_id}').json()['user']
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

    # Наладить тут с данными
    for test in req_data:
        tests.append({'title': test['name'], 'description': test['about'], 'questions': len(test['questions']),
                      'category': test['category']})

    print('success authorization')

    return render_template('welcome.html', lst=tests, username=current_user.get_data()['name'])


# Главная страница со всеми тестами
@app.route('/main', methods=['GET', 'POST'])
def main():
    params = {
        "list_of_tests": [
            {"title": "Первый тест", "description": "Биология", "questions": 3, "category": "Иван Сусанин"},
            {"title": 'Второй тест', "description": "Математика", "questions": 5, "category": "Марина"},
            {"title": 'Третий тест', "description": "Кулинария", "questions": 10, "category": "Биология"}]
    }

    print("main page opened")

    return render_template("main.html", **params)


@app.route('/search', methods=['GET', 'POST'])
def search():
    print("searching")

    name = request.form['name']
    # print(name)

    # Список словарей с подходиящими названиями
    lst = [{"title": "Первый тест", "description": "Биология", "questions": 3, "category": "Иван Сусанин"},
           {"title": 'Второй тест', "description": "Математика", "questions": 5, "category": "Марина"},
           {"title": 'Третий тест', "description": "Кулинария", "questions": 10, "category": "Биология"}]

    params = {"lst": lst,
              "name": name}

    return render_template('searching.html', **params)


# Личный кабинет
@app.route('/profile/stats', methods=['GET', 'POST'])
def stats():
    print("stats")

    params = current_user.get_data()['passed_tests']

    if str(params)[-1] == '1':
        message = 'Всего пройдено ' + str(params) + ' тест'

    elif str(params)[-1] == '2' or str(params)[-1] == '3' or str(params)[-1] == '4':
        message = 'Всего пройдено ' + str(params) + ' теста'

    else:
        message = 'Всего пройдено ' + str(params) + ' тестов'

    return render_template('stats.html', mess_with_count=message)


@app.route('/creating/question', methods=['GET', 'POST'])
def create_question():
    form = CreateQuestion()

    return render_template("creating_question.html", nums=range(int(request.form['num'])), int=int, form=form)


@app.route('/creating/types', methods=['GET', 'POST'])
def create_type():
    form = CreateType()

    types = [{'id': 1, 'text': 'обычный'},
             {'id': 2, 'text': 'выбор правильного ответа'},
             {'id': 3, 'text': 'выбор нескольких правильных ответов'}]

    # request.args['title']
    for i in range(int(request.args['count'])):
        form.type.append_entry()

    print(form.type)

    params = {
        'types': types,
        'int': int,
        'form': form,
        'count': range(int(request.args['count']))
    }

    # for field in form.type:
        # field.data

    # Это в validate_on_submit()

    if form.validate_on_submit():
        pass

    return render_template("creating_type.html", **params)


@app.route('/creating/thbc', methods=['GET', 'POST'])
def create_thbc():
    return render_template('test_have_been_created.html')


# Создание тестов
@app.route('/creating', methods=['GET', 'POST'])
def create():
    print("creating")

    form = Create()

    cats = ['Химия',
            'Физика',
            'География',
            'Биология',
            {'id': 5, 'text': 'Информатика'},
            {'id': 6, 'text': 'История'},
            {'id': 7, 'text': 'Алгебра'},
            {'id': 8, 'text': 'Геометрия'},
            {'id': 9, 'text': 'Геология'},
            {'id': 10, 'text': 'Астрономия'},
            {'id': 11, 'text': 'Информационные технологии'}]

    form.category.choices = cats
    form.type.choices = ['Открытый', 'Закрытый']

    if form.validate_on_submit():
        params = {'title': form.title.data,
                  'category': form.category.data,
                  'count': form.count.data,
                  'description': form.description.data,
                  'type': form.description.data}

        print('/creating/types?' + '&'.join([k + '=' + str(v) for k, v in params.items()]))
        return redirect('/creating/types?' + '&'.join([k + '=' + str(v) for k, v in params.items()]))

    return render_template('creating.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
