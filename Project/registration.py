from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class RegForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    login = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(8, -1, 'Недостаточно символов!')])
    submit = SubmitField('Зарегистрироваться')
