from datetime import datetime
import unittest
from flask_qrcode import QRcode
from flask_hashing import Hashing
# Importar Flask para poder trabajar con el
from flask import flash, make_response, redirect, render_template, url_for
from flask_login import current_user, login_required
from app import create_app
from app.forms import Todo, DeleteTodoForm, CreateVisit, DeleteVisit
from app.firebase_service import get_todos, put_todo, delete_todo, update_todo, put_visit, get_visits, delete_visit

app = create_app()  # Crear la app
QRcode(app)
hashing = Hashing(app)


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def not_found(error):
    return render_template('500.html', error=error)


def user_advance(user_todos):
    advance = 0
    for i in user_todos:
        todo = i.to_dict()
        if todo["done"]:
            advance += 1
    if advance == 0:
        return advance
    else:
        advance = (100 / len(user_todos)) * advance
    return round(advance, 2)


@app.route('/')  # Entrada a la app
def index():
    # Respuesta y redirección a home
    response = make_response(redirect('/home'))
    return response


@app.route('/home', methods=['GET', 'POST'])  # Primera ruta (Home)
# Protejemos la ruta con LoginRequired
@login_required
def home():
    username = current_user.id
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
    }  # Pasaremos contexto con varibles en vez de un diccionario, usamos ** para hacer de cada llave/valor una variable :D
    # Cuando recibamos el form le pasamos la descripción a put_todo
    if todo_form.is_submitted():
        put_todo(username, todo_form.description.data)
        flash('Tarea creada con éxito')
        return redirect(url_for('home'))

    # Responder al usuario con su IP en un template HTML
    return render_template('home.html', **context)
# Rutas dinámicas


@app.route('/delete_todos/<todo_id>', methods=['GET', 'POST'])
@login_required
def delete_todos(todo_id):
    username = current_user.id
    delete_todo(username, todo_id)

    return redirect(url_for('home'))


@app.route('/update_todos/<todo_id>/<int:done>', methods=['GET', 'POST'])
@login_required
def update_todos(todo_id, done):
    username = current_user.id
    update_todo(username, todo_id, done)

    return redirect(url_for('home'))


@app.route('/visitas', methods=['GET', 'POST'])
@login_required
def visitas():
    username = current_user.id
    user_visits = get_visits(username)
    visit_form = CreateVisit()
    delete_visit = DeleteVisit()
    context = {
        'visit_form': visit_form,
        'visits': user_visits,
        'delete_visit': delete_visit
    }

    if visit_form.is_submitted():
        dt = datetime.combine(visit_form.date.data, datetime.now().time())
        hashed_fields = hashing.hash_value(
            str(dt) + current_user.id, salt='flask-app')

        put_visit(username, dt, visit_form.visitor.data, hashed_fields)

        # Tenemos que mandar los datos recién capturados y hashear para manadar el qr
        flash('Visita creada con éxito')

        return redirect(url_for('visitas'))

    return render_template('visitas.html', **context)


@app.route('/delete_visits/<visit_id>', methods=['GET', 'POST'])
@login_required
def delete_visits(visit_id):
    username = current_user.id
    delete_visit(username, visit_id)

    return redirect(url_for('visitas'))


@app.route('/areas_comunes')
@login_required
def areas_comunes():
    return render_template('areas_comunes.html')


@app.route('/comunicacion')
@login_required
def comunicacion():
    return render_template('comunicacion.html')
