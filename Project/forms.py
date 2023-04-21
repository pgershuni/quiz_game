from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, FieldList
from wtforms.validators import DataRequired, Length


class RegForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    login = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(8, -1, 'Недостаточно символов!')])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class Create(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    category = SelectField('Категория', validators=[DataRequired()])
    count = IntegerField('Количество вопросов', validators=[DataRequired()])
    description = StringField('Описание')
    type = SelectField('Доступ', validators=[DataRequired()])
    submit = SubmitField('Следующий шаг')


class CreateType(FlaskForm):
    type = FieldList(SelectField('Тип вопроса', validators=[DataRequired()], choices=['обычный', 'выбор правильного ответа', 'выбор нескольких правильных ответов']))
    submit = SubmitField('Создание вопросов')


class CreateQuestion(FlaskForm):
    condition = StringField('Условие', validators=[DataRequired()])
    correct_answer = StringField('Правильный ответ', validators=[DataRequired()])
    submit = SubmitField('Создать тест')
