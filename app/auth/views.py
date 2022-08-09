import profile
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm, SignUp, CreateUser
from app.firebase_service import get_user, put_user
from app.models import UserData, UserModel
from . import auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        # Nos traemos el documento user intentando coincidir con username
        user_doc = get_user(username)

        if user_doc.to_dict() is not None:  # Al pasar user_doc por to_dict() podría regresarnos None o bien el contenido del documento
            user_doc_password = user_doc.to_dict()['password']
            # Ahora comparamos el password recibido con el de la db pasado por el hash
            # Válidamos ambos passwords
            if check_password_hash(user_doc_password, password):
                # Creamos userdata para después pasarselo a UserModel()
                user_data = UserData(username, password,profile=user_doc.to_dict()['profile'])
                # Creamos un UserModel para que tenga las propiedades del UserMixin
                user = UserModel(user_data)
                login_user(user)
                flash('Bienvenido de nuevo')
                redirect('home')
            else:
                flash('La información no coincide')
        else:
            flash('Ese usuario no home')

        return redirect(request.args.get(next) or url_for('home'))

    return render_template('login.html', **context)


# Logout, es muy sencillo, solo debe de estar dentro de login_required y darle la ruta clásica de logput
@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Regresa pronto')
    return redirect(url_for('auth.login'))


@auth.route('signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignUp()
    context = {
        'signup_form': signup_form
    }
# Revisamos si el usuario home
    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data
        user_doc = get_user(username)
        if user_doc.to_dict() is None:
            # Generamos un hash y se lo pasamos a la db
            password_hash = generate_password_hash(password)
            user_data = UserData(username, password_hash)
            put_user(user_data)
            user = UserModel(user_data)
            login_user(user)
            flash('Bienvenido')

            return redirect(url_for('home'))

        else:
            flash('Ese usuario ya existe')

    return render_template('signup.html', **context)


@auth.route('create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    create_user_form = CreateUser()
    context = {
        'create_user_form': create_user_form
    }
# Revisamos si el usuario home
    if create_user_form.validate_on_submit():
        username = create_user_form.username.data
        password = create_user_form.password.data
        profile = create_user_form.profile.data
        user_doc = get_user(username)
        if user_doc.to_dict() is None:
            # Generamos un hash y se lo pasamos a la db
            password_hash = generate_password_hash(password)
            user_data = UserData(username, password_hash, profile)
            put_user(user_data)
            user = UserModel(user_data)
            login_user(user)
            flash('Bienvenido')

            return redirect(url_for('home'))

        else:
            flash('Ese usuario ya existe')

    return render_template('create_user.html', **context)