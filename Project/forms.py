from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, FieldList, \
    RadioField, SelectMultipleField, FormField
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
    text = StringField('Условие', validators=[DataRequired()])
    options = FieldList(StringField('Вариант', validators=[DataRequired()]))
    true_answer = StringField('Правильный ответ', validators=[DataRequired()])


class CreateTest(FlaskForm):
    questions = FieldList(FormField(CreateQuestion))
    submit = SubmitField('Создать тест')


class OpenCommon(FlaskForm):
    text = StringField()
    answer = StringField('Ответ', validators=[DataRequired()])
    submit = SubmitField('Ответить')


class OpenRadio(FlaskForm):
    text = StringField()
    radio = RadioField(validators=[DataRequired()], choices=[])
    submit = SubmitField('Ответить')


class OpenCheckbox(FlaskForm):
    text = StringField()
    checkbox = SelectMultipleField(validators=[DataRequired()], choices=[])
    submit = SubmitField('Ответить')
