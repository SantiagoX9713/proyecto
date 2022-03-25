from ensurepip import bootstrap
from flask import flash, request,make_response,redirect,render_template,session,url_for # Importar Flask para poder trabajar con el
import unittest
from app import create_app
from app.forms import LoginForm


app = create_app() #Crear la app

todos = ['TODO','TODO 1','TODO 2']

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


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


@app.route('/hello',methods=['GET','POST']) #Primera ruta (Home)
def hello():
    user_ip = session.get('user_ip') #Leemos la session y obtenemos la IP
    login_form = LoginForm()
    username =  session.get('username')
    context = {
        'user_ip':user_ip,
        'todos':todos,
        'login_form': login_form,
        'username': username
    } # Pasaremos contexto con varibles en vez de un diccionario, usamos ** para hacer de cada llave/valor una variable :D
    
    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] = username
        flash('Usuario guardado exitosamente!')

        return redirect(url_for('index'))
    
    return render_template('hello.html',**context) # Responder al usuario con su IP en un template HTML

