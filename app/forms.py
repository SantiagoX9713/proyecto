from flask_wtf import FlaskForm
# from wtforms.widgets import DateTimeInput
from wtforms.fields import StringField, PasswordField, SubmitField, DateTimeField, HiddenField
from wtforms.validators import DataRequired, EqualTo, InputRequired


class LoginForm(FlaskForm):
    username = StringField('Nombre de Usuario',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Enviar')

# Un intento para hacer un formulario de registro :D
class SignUp(FlaskForm):
    username = StringField('Nombre de Usuario',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(), InputRequired(),EqualTo('password')])
    password_repeat = PasswordField('Repite tu Password',validators=[DataRequired(),InputRequired()])
    submit = SubmitField('Enviar')


# Creamos una nueva forma para agregar nuevos todos :D
class Todo(FlaskForm):
    description = StringField('Descripción', validators=[DataRequired()])
    submit = SubmitField('Guardar')


class DeleteTodoForm(FlaskForm):
    submit = SubmitField('Borrar')


class CreateVisit(FlaskForm):
    date = DateTimeField('Fecha de Visita', validators=[DataRequired()])
    visitor = StringField('Visitante(s)', validators=[DataRequired()])
#    hashed_fields = HiddenField('Campos hasheados')
    submit = SubmitField('Enviar')