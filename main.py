from ensurepip import bootstrap
from flask import Flask, request,make_response,redirect,render_template # Importar Flask para poder trabajar con el
from flask_bootstrap import Bootstrap
app = Flask(__name__) #Crear la app
bootstrap = Bootstrap(app)
todos = ['TODO','TODO 1','TODO 2']

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
    response.set_cookie('user_ip',user_ip) # Mandamos un cookie con la IP
    return response


@app.route('/hello') #Primera ruta (Home)
def hello():
    user_ip = request.cookies.get('user_ip') #Leemos la cookie y obtenemos la IP
    context = {
        "user_ip":user_ip,
        "todos":todos
    } # Pasaremos contexto con varibles en vez de un diccionario, usamos ** para hacer de cada llave/valor una variable :D
    return render_template('hello.html',**context) # Responder al usuario con su IP en un template HTML

