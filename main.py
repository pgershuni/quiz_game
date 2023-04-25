from flask import jsonify
from flask import make_response
from flask import Flask, url_for, request
from _data import _db_session
import random
import datetime
from flask_restful import reqparse, abort, Api, Resource
from _data.__all_models import Question, Test, Option, User, Telegram_key, Category

_db_session.global_init("db/tests.db")
db_sess = _db_session.create_session()

app = Flask('app')
api = Api(app)


def add_categories():
    categories = ['Химия',
                  'Физика',
                  'География',
                  'Биология',
                  'Информатика',
                  'История',
                  'Алгебра',
                  'Геометрия',
                  'Геология',
                  'Астрономия',
                  'Информационные технологии']

    for category in categories:
        cat = Category()
        cat.text = category

        db_sess.add(cat)
        db_sess.commit()


add_categories()


def add_option(text, question_id, is_correct):  # добавление в базу данных варианта выбора \ ответа
    opt = Option()
    opt.text = text
    opt.question_id = question_id
    opt.is_correct = is_correct
    db_sess.add(opt)
    db_sess.commit()


def add_question(question, answer, test_id, question_type='ord'):  # добавление в базу данных вопроса
    if not question:  # ошибка, которая возникает, если в вопросе не передан вопрос
        return 'error'
    if not answer:  # ошибка, которая возникает, если в вопросе не передан вопрос
        return 'error2'
    quest = Question()
    # вопрос считывается по-разному, в зависимости от его типа
    if question_type == 'ord':
        quest.question = question
    elif question_type == 'rad' or question_type == 'check':
        quest.question = question[0]
    else:  # если тип передан неверно, выводится соответствующая ошибка
        return 'error1'
    quest.type = question_type
    quest.test_id = test_id
    db_sess.add(quest)
    db_sess.commit()

    id = db_sess.query(Question).all()[-1].id  # получение id переданного вопроса
    if question_type == 'ord' or question_type == 'rad':  # добавление ответа в бд
        add_option(answer, id, True)
    if question_type == 'check' or question_type == 'rad':  # добавлеие в бд вариантов ответа\ответов, если их несколько
        if type(question) != list or len(question) != 2:  # проверка правильности структуры переданных вавриантов ответа
            return 'error'
        elif type(question[1]) != list:
            return 'error'
        for quest in question[1]:  # добавление вариантов ответа
            add_option(quest, id, False)
        if question_type == 'check':  # добавление ответов
            for text in answer:
                add_option(text, id, True)


def add_test(title, about, questions, user_id, is_private, category_text):  # добавление теста в бд

    test = Test()
    test.title = title
    test.about = about

    category = db_sess.query(Category).filter(Category.text == category_text).first()
    if category:
        test.category = category
    else:
        return 'bad category'

    test.key = random.randint(0, 1000000000)  # генерация ключа теста
    test.user_id = user_id
    test.is_private = is_private
    if not questions:  # проверка наличия вопросов
        return 'questions not passed'
    if not any([any([key in question.keys() for key in ['question', 'answer', 'type']]) for question in questions]):
        # проверка структуры вопросов
        return 'bad questions'
    db_sess.add(test)
    db_sess.commit()

    id = db_sess.query(Test).all()[-1].id
    for question in questions:  # создание вопросов
        res = add_question(question['question'], question['answer'], id, question['type'])
        # обработка ошибок
        if res == 'error':
            return 'bad questions'
        elif res == 'error1':
            return 'bad type'
        elif res == 'error2':
            return 'bad answer'
    return db_sess.query(Test).all()[-1].key


def add_user(name, about, login, password):  # добавление пользователя
    user = User()
    user.name = name
    user.about = about
    user.num_passed_tests = 0
    user.login = login
    user.password = password
    db_sess.add(user)
    db_sess.commit()
    return db_sess.query(User).all()[-1].id


def add_telegram_key(user_id):  # добавление телеграм ключа
    key = Telegram_key()
    key.user_id = user_id
    key.key = random.randint(1000000000000000, 9999999999999999)  # генерация ключа
    key.date = datetime.datetime.now()  # сохранение времени создания
    db_sess.add(key)
    db_sess.commit()
    return db_sess.query(Telegram_key).all()[-1].key


def get_question(question):  # получение вопросов (происходит по-разному в зависимости от типа)
    if question.type == 'check':
        result = {'type': question.type,
                  'question': [question.question,
                               [option.text for option in question.options if not option.is_correct]],
                  'answer': [option.text for option in question.options if option.is_correct]}
    elif question.type == 'rad':
        result = {'type': question.type,
                  'question': [question.question,
                               [option.text for option in question.options if not option.is_correct]],
                  'answer': [option.text for option in question.options if option.is_correct][0]}
    elif question.type == 'ord':
        result = {'type': question.type,
                  'question': question.question,
                  'answer': [option.text for option in question.options if option.is_correct][0]}
    return result


def get_test(test_key, all=False):  # получение тестов
    if all:  # получение всех тестов
        tests = db_sess.query(Test)
    else:  # получение теста по ключу
        tests = db_sess.query(Test).filter(Test.key == test_key)
    results = []

    for test in tests:  # создание ответа
        result = {'name': test.title,
                  'about': test.about,
                  'category': test.category.text,
                  'key': test.key,
                  'user_id': test.user_id,
                  'is_private': test.is_private,
                  'questions': [get_question(question) for question in test.questions]}
        results.append(result)

    if all:  # вывод всех тестов
        return results
    else:  # вывод теста по ключу
        return results[0]


def get_user(id, all=False):  # получение пользователя
    if all:  # получение всех пользователей
        users = db_sess.query(User)
    else:  # получение пользоателя по id
        users = db_sess.query(User).filter(User.id == id)
    result = []

    for user in users:  # создание ответа
        result.append({'id': user.id,
                       'passed_tests': user.num_passed_tests,
                       'name': user.name,
                       'about': user.about,
                       'telegram_key': user.telegram_key.key if user.telegram_key else None,
                       'login': user.login,
                       'password': user.password})
    if all:  # вывод всех тестов
        return result
    else:  # вывод теста по ключу
        return result[0]


def get_user_id_from_telegram_key(key):  # получение телеграмм люча
    tele_key = db_sess.query(Telegram_key).filter(Telegram_key.key == key)[0]
    if (datetime.datetime.now() - tele_key.date).total_seconds() > 600:  # вывод соответствующей ошибки, если ключ истёк
        return 'error'
    return tele_key.user_id


def get_categories():
    result = []
    categories = db_sess.query(Category)
    for category in categories:
        result.append({'text': category.text})
    return result


def abort_if_test_not_found(test_key):  # проверка наличия теста по ключу
    test = db_sess.query(Test).filter(Test.key == test_key).first()
    if not test:
        abort(404, message=f"Test {test_key} not found")


class TestResource(Resource):
    def get(self, test_key):  # обработчик получения теста по ключу
        abort_if_test_not_found(test_key)
        return jsonify(
            {
                'test':
                    get_test(test_key)
            }
        )

    def delete(self, test_key):  # обработчик удаления теста по ключу
        abort_if_test_not_found(test_key)
        test = db_sess.query(Test).filter(Test.key == test_key)[0]
        db_sess.delete(test)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class TestListResource(Resource):
    # создание парсера аргументов для добавления теста
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str)
    parser.add_argument('about', type=str)
    parser.add_argument('category', type=str)
    parser.add_argument('questions', action='append', type=dict)
    parser.add_argument('is_private', type=bool)
    parser.add_argument('user_id', type=int)

    def get(self):  # обработчик получения всех тестов
        return jsonify(
            {
                'tests':
                    get_test('', all=True)
            }
        )

    def post(self):  # обработчик добавления теста
        args = self.parser.parse_args()
        # создание теста
        res = add_test(args['title'],
                       args['about'],
                       args['questions'],
                       args['user_id'],
                       args['is_private'],
                       args['category'])
        if res == 'bad questions' or \
                res == 'bad type' or \
                res == 'questions not passed' or \
                res == 'bad answer' or \
                res == 'bad category':
            # обработка ошибок добавления
            abort(400, message=f'error, {res}')
        return jsonify({'success': 'OK', 'key': res})


def abort_if_user_not_found(user_id):  # проверка наличия пользователя по id
    user = db_sess.query(User).filter(User.id == user_id).first()
    if not user:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):  # обработчик получения пользователя по id
        abort_if_user_not_found(user_id)
        return jsonify(
            {
                'user': get_user(user_id)
            }
        )

    def delete(self, user_id):  # обработчик удаления пользователя по id
        abort_if_user_not_found(user_id)
        user = db_sess.query(User).filter(User.id == user_id)[0]
        db_sess.delete(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    # создание парсера аргументов для добавления пользователя
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('about', type=str)
    parser.add_argument('login', type=str)
    parser.add_argument('password', type=str)

    def get(self):  # обработчик получения всех пользователей
        return jsonify(
            {
                'users':
                    get_user('', all=True)
            }
        )

    def post(self):  # обработчик добавления пользователя
        args = self.parser.parse_args()
        res = add_user(args['name'], args['about'], args['login'], args['password'])
        return jsonify({'success': 'OK', 'id': res})


def abort_if_key_not_found(key):  # проверка наличия телеграмм ключа
    tele_key = db_sess.query(Telegram_key).filter(Telegram_key.key == key).first()
    if not tele_key:
        abort(404, message=f"key {key} not found")


class TelegramKeyResource(Resource):
    def get(self, key):  # обработчик получения id пользователя по телеграм ключу
        abort_if_key_not_found(key)
        user_id = get_user_id_from_telegram_key(key)

        if user_id == 'error':  # вывод ошибки, если ключ истек
            abort(400, message=f"key {key} is not valid")

        return jsonify(
            {
                'user': get_user_id_from_telegram_key(key)
            }
        )

    def delete(self, key):  # обработчик удаления телеграм ключа
        abort_if_key_not_found(key)
        tele_key = db_sess.query(Telegram_key).filter(Telegram_key.key == key)[0]
        db_sess.delete(tele_key)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class TelegramKeyListResource(Resource):
    # создание парсера аргументов для добавления ключа
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=str)

    def post(self):  # обработчик добавления ключа
        args = self.parser.parse_args()
        abort_if_user_not_found(args['user_id'])  # проверка наличия пользователя для которого генерируется ключ
        res = add_telegram_key(args['user_id'])
        return jsonify({'success': 'OK', 'key': res})


class Test_passed_Resource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        user = db_sess.query(User).filter(User.id == user_id)[0]
        user.num_passed_tests = user.num_passed_tests + 1
        db_sess.commit()
        return jsonify({'success': 'OK'})


class Categories_List_Resourse(Resource):
    def get(self):  # обработчик получения всех пользователей
        return jsonify(
            {
                'categories':
                    get_categories()
            }
        )


api.add_resource(Test_passed_Resource, '/api/passed_tests/<int:user_id>')
api.add_resource(Categories_List_Resourse, '/api/categories/')

# добавление обработчиков для api тестов
api.add_resource(TestListResource, '/api/tests')
api.add_resource(TestResource, '/api/tests/<int:test_key>')

# добавление обработчиков для api пользователей
api.add_resource(UserListResource, '/api/users')
api.add_resource(UserResource, '/api/users/<int:user_id>')

# добавление обработчиков для api телеграм ключей
api.add_resource(TelegramKeyListResource, '/api/telegram_keys')
api.add_resource(TelegramKeyResource, '/api/telegram_keys/<int:key>')
import db_test

app.run(port=8080)
