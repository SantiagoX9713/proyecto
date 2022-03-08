from flask import Flask, request,make_response,redirect,render_template # Importar Flask para poder trabajar con el

app = Flask(__name__) #Crear la app
todos = ['TODO','TODO 1','TODO 2']
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
    } # Pasaremos contexto con un diccionario
    return render_template('hello.html',context=context) # Responder al usuario con su IP en un template HTML

