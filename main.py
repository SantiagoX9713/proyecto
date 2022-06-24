from multiprocessing import context
import unittest
from flask_qrcode import QRcode
from flask import flash, make_response,redirect,render_template, url_for # Importar Flask para poder trabajar con el
from flask_login import current_user, login_required
from app import create_app
from app.forms import Todo, DeleteTodoForm, CreateVisit
from app.firebase_service import get_todos, put_todo, delete_todo, update_todo, put_visit

app = create_app() #Crear la app
QRcode(app)

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


def user_advance(user_todos):
    advance = 0
    for i in user_todos:
        todo = i.to_dict()
        if todo["done"]:
            advance += 1
    print(advance)
    if advance == 0:
        return advance
    else:
        advance = (100 / len(user_todos)) * advance
    return round(advance, 2)


@app.route('/') #Entrada a la app
def index():
    response = make_response(redirect('/home')) # Respuesta y redirección a home
    return response


@app.route('/home',methods=['GET', 'POST']) #Primera ruta (Home)
# Protejemos la ruta con LoginRequired
@login_required
def home():
    username =  current_user.id
    user_todos = get_todos(username)
    advance = user_advance(user_todos)
    todo_form = Todo()
    delete_form = DeleteTodoForm()
    context = {
        'todos': user_todos,
        'advance': advance,
        'username': username,
        'todo_form': todo_form,
        'delete_form': delete_form
        } # Pasaremos contexto con varibles en vez de un diccionario, usamos ** para hacer de cada llave/valor una variable :D
    # Cuando recibamos el form le pasamos la descripción a put_todo
    if todo_form.is_submitted():
        put_todo(username,todo_form.description.data)
        flash('Tarea creada con éxito')
        return redirect(url_for('home'))
  
    return render_template('home.html',**context) # Responder al usuario con su IP en un template HTML
# Rutas dinámicas
@app.route('/todos/delete/<todo_id>', methods=['GET', 'POST'])
@login_required
def delete(todo_id):
    username = current_user.id
    delete_todo(username, todo_id)
    
    return redirect(url_for('home'))


@app.route('/todos/update/<todo_id>/<int:done>', methods=['GET','POST'])
@login_required
def update(todo_id, done):
    username = current_user.id
    update_todo(username, todo_id, done)
    
    return redirect(url_for('home'))


@app.route('/visitas')
@login_required
def visitas():
    visit_form = CreateVisit()
    context = {
        'visit': visit_form
    }
    if visit_form.is_submitted():
        put_visit(current_user.id,visit_form.date.data, visit_form.visitor.data)
        return render_template('visitas.html')#Tenemos que mandar los datos recién capturados y hasear para manadar el qr
        
    return render_template('visitas.html', **context)



@app.route('/areas_comunes')
@login_required
def areas_comunes():
    return render_template('areas_comunes.html')


@app.route('/comunicacion')
@login_required
def comunicacion():
    return render_template('comunicacion.html')
