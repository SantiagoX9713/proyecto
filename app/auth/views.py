from flask import render_template,flash,redirect,url_for,session
from flask_login import login_user, login_required, logout_user
from app.forms import LoginForm
from app.firebase_service import get_user
from app.models import UserData, UserModel
from . import auth

@auth.route('/login',methods=['GET','POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form' : login_form
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user_doc = get_user(username)# Nos traemos el documento user intentando coincidir con username
        
        if user_doc.to_dict() is not None:# Al pasar user_doc por to_dict() podría regresarnos None o bien el contenido del documento
            user_doc_password = user_doc.to_dict()['password']
            if password == user_doc_password:# Válidamos ambos passwords
                user_data = UserData(username,password)# Creamos userdata para después pasarselo a UserModel()
                user = UserModel(user_data)# Creamos un UserModel para que tenga las propiedades del UserMixin
                login_user(user)
                flash('Bienvenido de nuevo')
                redirect('hello')
            else:
                flash('La información no coincide')
        else:
            flash('Ese usuario no existe')

        return redirect(url_for('index'))
   
    return render_template('login.html',**context)


# Logout, es muy sencillo, solo debe de estar dentro de login_required y darle la ruta clásica de logput
@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Regresa pronto')
    return redirect(url_for('auth.login'))