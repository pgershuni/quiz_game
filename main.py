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


def add_option(text):
    opt = Option()
    opt.text = text
    db_sess.add(opt)
    db_sess.commit()
    return db_sess.query(Option).all()[-1].id


def add_question(question, answer, type='ord'):
    quest = Question()

    if type == 'ord':
        quest.question = question
        quest.answer = answer
    elif type == 'rad':
        quest.question = question[0]
        quest.questions = ','.join([str(add_option(text)) for text in question[1]])
        quest.answer = answer
    elif type == 'check':
        quest.question = question[0]
        quest.questions = ','.join([str(add_option(text)) for text in question[1]])
        quest.answer = ','.join([str(add_option(text)) for text in answer])

    quest.type = type
    db_sess.add(quest)
    db_sess.commit()
    return db_sess.query(Question).all()[-1].id


def add_test(name, about, questions, user, private):
    test = Test()
    test.name = name
    test.about = about
    test.key = random.randint(0, 1000000000)
    test.user = user
    print(questions, name, about, user, private)
    if not any([any([key in question.keys() for key in ['question', 'answer', 'type']]) for question in questions]):
        return 'bad questions'
    test.questions = ','.join([str(add_question(question['question'],
                                                question['answer'],
                                                question['type'])) for question in questions])
    if 'error' in test.questions:
        return 'bad questions'
    db_sess.add(test)
    db_sess.commit()
    return db_sess.query(Test).all()[-1].key


def add_user(name, about):
    user = User()
    user.name = name
    user.about = about
    db_sess.add(user)
    db_sess.commit()
    return db_sess.query(User).all()[-1].id


def get_option(id):
    option = db_sess.query(Option).filter(Option.id == int(id))[0]
    return option.text


def get_question(id):
    question = db_sess.query(Question).filter(Question.id == id)[0]
    if question.type == 'check':
        result = {'type': question.type,
                 'question': [question.question, [get_option(id) for id in question.questions.split(',')]],
                 'answer': [get_option(id) for id in question.answer.split(',')]}
    elif question.type == 'rad':
        result = {'type': question.type,
                 'question': [question.question, [get_option(id) for id in question.questions.split(',')]],
                 'answer': question.answer}
    elif question.type == 'ord':
        result = {'type': question.type,
                 'question': question.question,
                 'answer': question.answer}
    return result


def get_test(test_key, id=None, name=None, all=False):
    if id is not None:
        tests = db_sess.query(Test).filter(Test.id == id)
    if name is not None:
        tests = db_sess.query(Test).filter(Test.name == name)
    elif all:
        tests = db_sess.query(Test)
    else:
        tests = db_sess.query(Test).filter(Test.key == test_key)
    results = []
    for test in tests:
        result = {'name': test.name,
                  'about': test.about,
                  'questions': [get_question(id) for id in test.questions.split(',')]}
        results.append(result)
    if all:
        return results
    else:
        return results[0]


def get_user(id, test_name=''):
    if id:
        test = db_sess.query(Test).filter(Test.id == id)[0]
    else:
        test = db_sess.query(Test).filter(Test.name == test_name)[0]
    result = {'name': test.name,
              'about': test.about,
              'questions': [get_question(id) for id in test.questions.split(',')]}
    return result




def abort_if_test_not_found(test_key):
    news = db_sess.query(Test).filter(Test.key == test_key).first()
    if not news:
        abort(404, message=f"News {test_key} not found")


class TestResource(Resource):
    def get(self, test_key):
        abort_if_test_not_found(test_key)
        return jsonify(
            {
                'tests':
                    [get_test(test_key)]
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
                    [get_test('', all=True)]
            }
        )

    def post(self):
        args = self.parser.parse_args()
        res = add_test(args['title'], args['about'], args['questions'], args['user_id'], args['is_private'])
        if res == 'bad questions':
            return jsonify({'success': 'error, bad questions'})
        return jsonify({'success': 'OK', 'key': res})

# для списка объектов
api.add_resource(TestListResource, '/api/tests')

# для одного объекта
api.add_resource(TestResource, '/api/tests/<int:test_key>')

app.run(port=8080)
