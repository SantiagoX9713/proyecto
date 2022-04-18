import unittest
from ensurepip import bootstrap
from flask import flash, request,make_response,redirect,render_template,session,url_for # Importar Flask para poder trabajar con el
from flask_login import current_user, login_required
from app import create_app
from app.forms import Todo, DeleteTodoForm, UpdateTodoForm
from app.firebase_service import get_todos, put_todo, delete_todo, update_todo

app = create_app() #Crear la app


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


@app.route('/hello',methods=['GET', 'POST']) #Primera ruta (Home)
# Protejemos la ruta con LoginRequired
@login_required
def hello():
    user_ip = session.get('user_ip') #Leemos la session y obtenemos la IP
    username =  current_user.id
    todo_form = Todo()
    delete_form = DeleteTodoForm()
    update_form = UpdateTodoForm()
    context = {
        'user_ip':user_ip,
        'todos':get_todos(username),
        'username': username,
        'todo_form': todo_form,
        'delete_form': delete_form,
        'update_form': update_form
    } # Pasaremos contexto con varibles en vez de un diccionario, usamos ** para hacer de cada llave/valor una variable :D
    # Cuando recibamos el form le pasamos la descripción a put_todo
    if todo_form.is_submitted():
        put_todo(username,todo_form.description.data)
        flash('Tarea creada con éxito')
        return redirect(url_for('hello'))
  
    return render_template('hello.html',**context) # Responder al usuario con su IP en un template HTML
# Rutas dinámicas
@app.route('/todos/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    username = current_user.id
    delete_todo(username, todo_id)
    
    return redirect(url_for('hello'))


@app.route('/todos/update/<todo_id>/<int:done>', methods=['POST'])
def update(todo_id, done):
    username = current_user.id
    update_todo(username, todo_id, done)
    
    return redirect(url_for('hello'))