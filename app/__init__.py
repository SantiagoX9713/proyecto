from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from .config import Config
from .auth import auth
from .models import UserModel
# Instanciamos el LoginManager
login_manager = LoginManager()
# Le decimos cual es la ruta en la que se hará login
login_manager.login_view = 'auth.login'

# Modelo de user


@login_manager.user_loader
def load_user(username):
    return UserModel.query(username)


def create_app():
    app = Flask(__name__)  # Crear la app
    bootstrap = Bootstrap(app)
    app.config.from_object(Config)
    # Inicialicamos la app con el LoginManager
    login_manager.init_app(app)
    app.register_blueprint(auth)
    return app
