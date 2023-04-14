import sqlalchemy
from sqlalchemy import orm
from ._db_session import SqlAlchemyBase


class Test(SqlAlchemyBase):
    __tablename__ = 'tests'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Users.id'))
    key = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
    author = orm.relationship('User', backref='tests')
    # questions


class Question(SqlAlchemyBase):
    __tablename__ = 'Questions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    question = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    test_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('tests.id'))

    test = orm.relationship('Test', backref='questions')
    # options


class User(SqlAlchemyBase):
    __tablename__ = 'Users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    telegram_key = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # tests


class Option(SqlAlchemyBase):
    __tablename__ = 'Options'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    question_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Questions.id'))
    is_correct = sqlalchemy.Column(sqlalchemy.Boolean)

    question = orm.relationship('Question', backref='options')


class Telegram_key(SqlAlchemyBase):
    __tablename__ = 'Telegram_keys'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    key = sqlalchemy.Column(sqlalchemy.String, nullable=False)

