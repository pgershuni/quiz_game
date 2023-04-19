import sqlalchemy
from sqlalchemy import orm
from ._db_session import SqlAlchemyBase


class Test(SqlAlchemyBase):
    __tablename__ = 'tests'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    category_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('categories.id'))
    key = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)

    author = orm.relationship('User', backref='tests')
    questions = orm.relationship('Question', back_populates='test', cascade='all')
    category = orm.relationship('Category', back_populates='tests')


class Question(SqlAlchemyBase):
    __tablename__ = 'questions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    question = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    test_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('tests.id'))

    test = orm.relationship('Test',  back_populates='questions')
    options = orm.relationship('Option', back_populates='question', cascade='all')


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    num_passed_tests = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    telegram_key = orm.relationship('Telegram_key', back_populates='user', uselist=False, cascade='all')
    # tests


class Option(SqlAlchemyBase):
    __tablename__ = 'options'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    question_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('questions.id'))
    is_correct = sqlalchemy.Column(sqlalchemy.Boolean)

    question = orm.relationship('Question', back_populates='options')


class Telegram_key(SqlAlchemyBase):
    __tablename__ = 'telegram_keys'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    key = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user = orm.relationship('User', back_populates='telegram_key')


class Category(SqlAlchemyBase):
    __tablename__ = 'categories'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    tests = orm.relationship('Test', back_populates='category')