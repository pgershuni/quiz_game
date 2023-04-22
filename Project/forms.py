from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, FieldList, \
    RadioField, SelectMultipleField
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
    category = SelectField('Категория', validators=[DataRequired()], choices=['Химия',
                                                                              'Физика',
                                                                              'География',
                                                                              'Биология',
                                                                              'Информатика',
                                                                              'История',
                                                                              'Алгебра',
                                                                              'Геометрия',
                                                                              'Геология',
                                                                              'Астрономия',
                                                                              'Информационные технологии'])
    count = IntegerField('Количество вопросов', validators=[DataRequired()])
    description = StringField('Описание')
    type = SelectField('Доступ', validators=[DataRequired()], choices=['Открытый', 'Закрытый'])
    submit = SubmitField('Следующий шаг')


class CreateType(FlaskForm):
    type = FieldList(SelectField('Тип вопроса', validators=[DataRequired()],
                                 choices=['обычный', 'выбор правильного ответа',
                                          'выбор нескольких правильных ответов']))

    submit = SubmitField('Создание вопросов')


class CreateQuestion(FlaskForm):
    question = FieldList(StringField('Условие', validators=[DataRequired()]),
                         StringField('Правильный ответ', validators=[DataRequired()]))


class CreateQuestionCommon(FlaskForm):
    common = FieldList(StringField('Условие', validators=[DataRequired()]),
                       StringField('Правильный ответ', validators=[DataRequired()]))


class CreateQuestionRadio(FlaskForm):
    radio = FieldList(StringField('Вариант 1', validators=[DataRequired()]),
                      StringField('Вариант 2', validators=[DataRequired()]),
                      StringField('Вариант 3', validators=[DataRequired()]),
                      StringField('Правильный ответ', validators=[DataRequired()]))


class CreateQuestionCheckbox(FlaskForm):
    checkbox = FieldList(StringField('Вариант 1', validators=[DataRequired()]),
                         StringField('Вариант 2', validators=[DataRequired()]),
                         StringField('Вариант 3', validators=[DataRequired()]),
                         StringField('Правильный ответ', validators=[DataRequired()]))


class CreateQuestionSubmit(FlaskForm):
    submit = SubmitField('Создать тест')
