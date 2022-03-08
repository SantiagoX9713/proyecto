from flask import Flask, request,make_response,redirect # Importar Flask para poder trabajar con el

app = Flask(__name__) #Crear la app

@app.route('/') #Entrada a la app
def index():
    user_ip = request.remote_addr #Obtener la IP del Usuario
    response = make_response(redirect('/hello')) # Respuesta y redirección a Hello
    response.set_cookie('user_ip',user_ip) # Mandamos un cookie con la IP
    return response


@app.route('/hello') #Primera ruta (Home)
def hello():
    user_ip = request.cookies.get('user_ip') #Leemos la cookie y obtenemos la IP
    return 'Tu IP es {}'.format(user_ip) # Responder al usuario con su IP

