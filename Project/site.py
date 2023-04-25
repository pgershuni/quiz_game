import itertools
import random

import requests
from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from forms import LoginForm, RegForm, Create, CreateType, CreateTest, OpenCommon, OpenRadio, OpenCheckbox

app = Flask('app')
app.config['SECRET_KEY'] = 'secretkeyandexlyceum'
url = 'https://agate-wool-teeth.glitch.me/'

# Доделать:
# - Проверка наличия теста с таким же именем
# - Открытие тестов

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"


@login_manager.user_loader
def load_user(user_id):
    user = requests.get(f'{url}api/users/{user_id}').json()['user']
    # print(user)
    return User(user)


class User(UserMixin):

    def __init__(self, data):
        self._id = data['id']
        self._data = data

    def get_id(self):
        return self._id

    def get_data(self):
        return self._data


@app.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect('/login')


@app.route('/')
def start():
    return redirect('/login')


@app.route('/check_data/<_type>', methods=['GET', 'POST'])
def check_data(_type):
    req_data = requests.get(f'{url}api/users').json()['users']
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
            user_id = requests.post(f'{url}api/users', json={'name': request.form['username'],
                                                             'about': '-',
                                                             'login': request.form['login'],
                                                             'password': request.form['password']
                                                             }).json()['id']
            # print(user_id, requests.get(f'http://127.0.0.1:8080/api/users/{user_id}').json())
            user = requests.get(f'{url}api/users/{user_id}').json()['user']
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
@login_required
def welcome():
    req_data = requests.get(f'{url}api/tests').json()['tests']

    tests = []
    for test in req_data:
        tests.append({'name': test['name'], 'description': test['about'], 'questions': len(test['questions']),
                      'category': test['category'], 'key': test['key']})

    tests = random.choices(tests, k=3)

    print('success authorization')

    return render_template('welcome.html', lst=tests, username=current_user.get_data()['name'])


# Главная страница со всеми тестами
@app.route('/main', methods=['GET', 'POST'])
@login_required
def main():
    req_data = requests.get(f'{url}api/tests').json()['tests']

    tests = []
    for test in req_data:
        tests.append({'name': test['name'], 'description': test['about'], 'questions': len(test['questions']),
                      'category': test['category'], 'key': test['key']})

    print("main page opened")

    return render_template("main.html", list_of_tests=tests)


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    print("searching")

    lst = requests.get(f'{url}api/tests').json()['tests']
    name = request.form['name']

    params = {
        "lst": lst,
        "name": name,
        "len": len
    }

    return render_template('searching.html', **params)


# Личный кабинет
@app.route('/profile/stats', methods=['GET', 'POST'])
@login_required
def stats():
    print("stats")

    params = current_user.get_data()['passed_tests']

    if str(params)[-1] == '1':
        message = 'Всего пройдено ' + str(params) + ' тест'

    elif str(params)[-1] == '2' or str(params)[-1] == '3' or str(params)[-1] == '4':
        message = 'Всего пройдено ' + str(params) + ' теста'

    else:
        message = 'Всего пройдено ' + str(params) + ' тестов'

    lst = requests.get(f'{url}api/tests').json()['tests']

    if 'tg_key' in request.args:
        params = {
            'mess_with_count': message,
            'len': len,
            'lst': lst,
            'user_id': current_user.get_data()['id'],
            'tg_key': request.args['tg_key']
        }
    else:
        params = {
            'mess_with_count': message,
            'len': len,
            'lst': lst,
            'user_id': current_user.get_data()['id']
        }

    return render_template('stats.html', **params)


@app.route('/creating', methods=['GET', 'POST'])
@login_required
def create():
    print("creating")

    form = Create()

    if form.validate_on_submit():

        errs = []
        gg = 0
        nn = 0
        if int(form.count.data) <= 0:
            gg += 1
            errs = ['Введите корректное количество вопросов']

        params = {'title': form.title.data,
                  'category': form.category.data,
                  'count': form.count.data,
                  'description': form.description.data,
                  'type': form.type.data}

        for test in requests.get(f'{url}api/tests').json()['tests']:
            if test['name'] == params['title']:
                gg += 1
                break

        if gg == 0:
            return redirect('/creating/types?' + '&'.join([k + '=' + str(v) for k, v in params.items()]))

        elif gg == 2:
            return render_template('creating.html', form=form, errors=['Тест с таким названием уже существует!'],
                                   errs=errs)
        elif gg == 0 and nn == 1:
            return render_template('creating.html', form=form, errs=errs)
        else:
            return render_template('creating.html', form=form, errors=['Тест с таким названием уже существует!'],
                                   )

    return render_template('creating.html', form=form)


@app.route('/creating/types', methods=['GET', 'POST'])
@login_required
def create_type():
    print('creating type')
    form = CreateType()

    types = [{'id': 1, 'text': 'обычный'},
             {'id': 2, 'text': 'выбор правильного ответа'},
             {'id': 3, 'text': 'выбор нескольких правильных ответов'}]

    params = {
        'types': types,
        'int': int,
        'form': form,
        'count': range(int(request.args['count']))
    }

    if form.validate_on_submit():
        params = {
            'count': range(int(request.args['count'])),
            'types': [elem.data for elem in form.type],
            'title': request.args['title'],
            'category': request.args['category'],
            'description': request.args['description'],
            'type': request.args['type']
        }
        # print('/creating/question?' + '&'.join([k + '=' + str(v) for k, v in params.items()]))
        return redirect('/creating/question?' + '&'.join([k + '=' + str(v) for k, v in params.items()]))

    for i in range(int(request.args['count'])):
        form.type.append_entry()

    return render_template("creating_type.html", **params)


@app.route('/creating/question', methods=['GET', 'POST'])
@login_required
def create_question():
    print('creating questions')
    form = CreateTest()

    types = request.args['types'][1:-1].replace("'", "").split(', ')

    params = {
        'types': types,
        'int': int,
        'form': form,
        'it': itertools
    }

    # Здесь нужно все заносить в бд
    if form.validate_on_submit():

        questions = []
        index = 0
        for elem in form.data['questions']:
            _type = types[index]

            if _type == 'обычный':
                time = {'answer': elem['true_answer'], 'question': elem['text'], 'type': 'ord'}
                questions.append(time)

            elif _type == 'выбор правильного ответа':
                time = {'answer': elem['true_answer'],
                        'question': [elem['text'], elem['options']],
                        'type': 'rad'}

                questions.append(time)

            else:
                time = {'answer': elem['true_answer'],
                        'question': [elem['text'], elem['options']],
                        'type': 'check'}

                questions.append(time)

            index += 1

        params = {
            'title': request.args['title'],
            'category': request.args['category'],
            'is_private': True if request.args['type'] == 'Открытый' else False,
            'about': request.args['description'],
            'questions': questions,
            'user_id': current_user.get_data()['id']
        }

        requests.post(f"{url}api/tests", json=params)

        return redirect('/creating/thbc')

    for elem in range(types.count('обычный')):
        form.questions.append_entry()

    for elem in range(types.count('выбор правильного ответа')):
        form.questions.append_entry()
        for q in range(3):
            form.questions[-1].options.append_entry()
            form.questions[-1].options[-1].label = f'Вариант {q + 1}'

    for elem in range(types.count('выбор нескольких правильных ответов')):
        form.questions.append_entry()
        for q in range(3):
            form.questions[-1].options.append_entry()
            form.questions[-1].options[-1].label = f'Вариант {q + 1}'

    return render_template("creating_question.html", **params)


@app.route('/creating/thbc', methods=['GET', 'POST'])
@login_required
def create_thbc():
    print('test have been created')

    return render_template('test_have_been_created.html')


@app.route('/test_open/<key>/<question_index>', methods=['GET', 'POST'])
@login_required
def test_open(key, question_index):
    test = requests.get(f'{url}api/tests/{key}').json()['test']
    questions = test['questions']

    print(f'test {key} have been opened')

    form_common = OpenCommon()
    form_radio = OpenRadio()
    form_checkbox = OpenCheckbox()

    if 'ta' not in request.args:
        return redirect(f"/test_open/{key}/0" + f'?ta={0}')

    try:
        params = {
            'title': test['name'],
            'question': questions[int(question_index)],
            'form': '',
            'type': questions[int(question_index)]['type'],
            '_choices': []
        }

        if params['type'] == 'ord':
            form_common.text.label = params['question']['question']
            params['form'] = form_common

        else:

            params['_choices'] = params['question']['question'][1]
            if params['type'] == "rad":
                params['form'] = form_radio
                form_radio.text.label = params['question']['question'][0]
                form_radio.radio.choices = params['question']['question'][1]

            else:
                params['form'] = form_checkbox
                form_checkbox.text.label = params['question']['question'][0]
                form_checkbox.checkbox.choices = params['question']['question'][1]

        # Тут же проверять ответ
        if params['form'].validate_on_submit():
            ta = int(request.args['ta'])
            if params['type'] == 'ord':
                if params['form'].data['answer'] == params['question']['answer']:
                    ta += 1

            else:
                if params['type'] == "rad":
                    if params['form'].radio.data == params['question']['answer']:
                        ta += 1
                else:
                    if set(params['form'].checkbox.data) == set(params['question']['answer']):
                        ta += 1
            return redirect(f"/test_open/{key}/{int(question_index) + 1}" + f'?ta={ta}')

    except IndexError:
        return redirect(f'/test_passed/{len(questions)}/{request.args["ta"]}')

    return render_template("test_open.html", **params)


@app.route('/test_passed/<count>/<ta>', methods=['GET', 'POST'])
def test_passed(count, ta):
    params = {
        'percent': int(int(ta) / int(count) * 100)
    }

    requests.get(f"{url}api/passed_tests/{current_user.get_data()['id']}")

    return render_template("test_passed.html", **params)


@app.route('/profile/create_tg_key', methods=['GET', 'POST'])
def create_tg_key():
    response = requests.post(f"{url}api/telegram_keys", json={'user_id': current_user.get_data()['id']})
    tg_key = response.json()['key']
    print(tg_key)
    return redirect("/profile/stats" + f"?tg_key={tg_key}")


if __name__ == '__main__':
    app.run(debug=True)
