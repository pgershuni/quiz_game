from flask import jsonify
from flask import make_response
from flask import Flask, url_for, request
from data import _db_session
import random
from flask_restful import reqparse, abort, Api, Resource
from data.__all_models import Question, Test, Option, User
_db_session.global_init("db/tests.db")
db_sess = _db_session.create_session()

app = Flask('app')
api = Api(app)


def add_option(text, question_id, is_correct):
    opt = Option()
    opt.text = text
    opt.question_id = question_id
    opt.is_correct = is_correct
    db_sess.add(opt)
    db_sess.commit()


def add_question(question, answer, test_id, question_type='ord'):
    if not question:
        return 'error'
    if not answer:
        return 'error2'
    quest = Question()
    if question_type == 'ord':
        quest.question = question
    elif question_type == 'rad' or question_type == 'check':
        quest.question = question[0]
    else:
        return 'error1'
    quest.type = question_type
    quest.test_id = test_id
    db_sess.add(quest)
    db_sess.commit()

    id = db_sess.query(Question).all()[-1].id
    if question_type == 'ord' or question_type == 'rad':
        add_option(answer, id, True)
    if question_type == 'check' or question_type == 'rad':
        print(type(question))
        if type(question) != list or len(question) != 2:
            return 'error'
        elif type(question[1]) != list:
            return 'error'
        for quest in question[1]:
            add_option(quest, id, False)
        if question_type == 'check':
            for text in answer:
                add_option(text, id, True)


def add_test(title, about, questions, user_id, is_private):
    test = Test()
    test.title = title
    test.about = about
    test.key = random.randint(0, 1000000000)
    test.user_id = user_id
    test.is_private = is_private
    if not questions:
        return 'questions not passed'
    if not any([any([key in question.keys() for key in ['question', 'answer', 'type']]) for question in questions]):
        return 'bad questions'
    db_sess.add(test)
    db_sess.commit()

    id = db_sess.query(Test).all()[-1].id
    for question in questions:
        res = add_question(question['question'], question['answer'], id, question['type'])

        if res == 'error':
            return 'bad questions'
        elif res == 'error1':
            return 'bad type'
        elif res == 'error2':
            return 'bad answer'
    return db_sess.query(Test).all()[-1].key


def add_user(name, about, login, password):
    user = User()
    user.name = name
    user.about = about
    user.telegram_key = '123'
    user.login = login
    user.password = password
    db_sess.add(user)
    db_sess.commit()
    return db_sess.query(User).all()[-1].id


def get_question(question):
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


def get_test(test_key, id=None, name=None, all=False):
    if id is not None:
        tests = db_sess.query(Test).filter(Test.id == id)
    if name is not None:
        tests = db_sess.query(Test).filter(Test.title == name)
    elif all:
        tests = db_sess.query(Test)
    else:
        tests = db_sess.query(Test).filter(Test.key == test_key)
    results = []

    for test in tests:
        result = {'name': test.title,
                  'about': test.about,
                  'key': test.key,
                  'user_id': test.user_id,
                  'is_private': test.is_private,
                  'questions': [get_question(question) for question in test.questions]}
        results.append(result)

    if all:
        return results
    else:
        return results[0]


def get_user(id, all=False):
    if all:
        users = db_sess.query(User)
    else:
        users = db_sess.query(User).filter(User.id == id)
    result = []

    for user in users:
        result.append({'id': user.id,
                  'name': user.name,
                  'about': user.about,
                  'telegram_key': user.telegram_key,
                  'login': user.login,
                  'password': user.password})
    if all:
        return result
    else:
        return result[0]


def abort_if_test_not_found(test_key):
    test = db_sess.query(Test).filter(Test.key == test_key).first()
    if not test:
        abort(404, message=f"Test {test_key} not found")


class TestResource(Resource):
    def get(self, test_key):
        abort_if_test_not_found(test_key)
        return jsonify(
            {
                'test':
                    get_test(test_key)
            }
        )

    def delete(self, test_key):
        abort_if_test_not_found(test_key)
        test = db_sess.query(Test).filter(Test.key == test_key)[0]
        db_sess.delete(test)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class TestListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str)
    parser.add_argument('about', type=str)
    parser.add_argument('questions', action='append', type=dict)
    parser.add_argument('is_private', type=bool)
    parser.add_argument('user_id', type=int)

    def get(self):
        return jsonify(
            {
                'tests':
                    get_test('', all=True)
            }
        )

    def post(self):
        args = self.parser.parse_args()
        res = add_test(args['title'], args['about'], args['questions'], args['user_id'], args['is_private'])
        if res == 'bad questions' or res == 'bad type' or res == 'questions not passed' or res == 'bad answer':
            abort(400, message=f'error, {res}')
        return jsonify({'success': 'OK', 'key': res})


def abort_if_user_not_found(user_id):
    user = db_sess.query(User).filter(User.id == user_id).first()
    if not user:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        return jsonify(
            {
                'user': get_user(user_id)
            }
        )

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        user = db_sess.query(User).filter(User.id == user_id)[0]
        db_sess.delete(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('about', type=str)
    parser.add_argument('login', type=str)
    parser.add_argument('password', type=str)

    def get(self):
        return jsonify(
            {
                'users':
                    [get_user('', all=True)]
            }
        )

    def post(self):
        args = self.parser.parse_args()
        res = add_user(args['name'], args['about'], args['login'], args['password'])
        return jsonify({'success': 'OK', 'id': res})

# для списка объектов
api.add_resource(TestListResource, '/api/tests')

# для одного объекта
api.add_resource(TestResource, '/api/tests/<int:test_key>')

# для списка объектов
api.add_resource(UserListResource, '/api/users')

# для одного объекта
api.add_resource(UserResource, '/api/users/<int:user_id>')

app.run(port=8080)
