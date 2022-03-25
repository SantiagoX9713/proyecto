from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/auth')#Las rutas que comienzen con auth serán redirigidas a este Blueprint

from . import views

