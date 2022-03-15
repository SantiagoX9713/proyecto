from ensurepip import bootstrap
from flask import Flask, request,make_response,redirect,render_template,session # Importar Flask para poder trabajar con el
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
app = Flask(__name__) #Crear la app
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'SUPER SECRETO'

todos = ['TODO','TODO 1','TODO 2']


class LoginForm(FlaskForm):
    username = StringField('Nombre de Usuario',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Enviar')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html',error=error)


@app.errorhandler(500)
def not_found(error):
    return render_template('500.html',error=error)


@app.route('/') #Entrada a la app
def index():
    user_ip = request.remote_addr #Obtener la IP del Usuario
    response = make_response(redirect('/hello')) # Respuesta y redirección a Hello
    session['user_ip'] = user_ip # Mandamos un session con la IP
    return response


@app.route('/hello') #Primera ruta (Home)
def hello():
    user_ip = session.get('user_ip') #Leemos la session y obtenemos la IP
    login_form = LoginForm()
    context = {
        'user_ip':user_ip,
        'todos':todos,
        'login_form': login_form
    } # Pasaremos contexto con varibles en vez de un diccionario, usamos ** para hacer de cada llave/valor una variable :D
    return render_template('hello.html',**context) # Responder al usuario con su IP en un template HTML

