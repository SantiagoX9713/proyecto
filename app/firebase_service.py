import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Login y comunicación con nuestro proyecto de GCP
credential = credentials.ApplicationDefault()
firebase_admin .initialize_app(credential)

# Instancia de Firestore
db = firestore.client()

# Primera función para obtener colecciones de Firestore
# Para obtener el usuario
def get_users():
    return db.collection('users').get()


def get_user(user_id):
    return db.collection('users').document(user_id).get()


# Para obtener los todos del usuario user_id
def get_todos(user_id):
    return db.collection('users').document(user_id).collection('todos').get()
# collection() para saber a que coleccion entrar y después obtener
# los documentos todos y con get() traemos toda la colección