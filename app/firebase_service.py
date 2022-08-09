from datetime import datetime
import firebase_admin
from google.cloud import firestore
from firebase_admin import credentials
from firebase_admin import firestore

# Login y comunicación con nuestro proyecto de GCP
credential = credentials.ApplicationDefault()
firebase_admin .initialize_app(credential)

# Instancia de Firestore
db = firestore.client()

# Primera función para obtener colecciones de Firestore


def get_user(user_id):
    return db.collection('users').document(user_id).get()


# Crear docuemento users
def put_user(user_data):
    user_ref = db.collection('users').document(user_data.username)
    user_ref.set({
        'password': user_data.password,
        'profile': user_data.profile
        })

# Para obtener los todos del usuario user_id


def get_todos(user_id):
    return db.collection('users').document(user_id).collection('todos').order_by('creation', direction=firestore.Query.DESCENDING).get()
# collection() para saber a que coleccion entrar y después obtener
# los documentos todos y con get() traemos toda la colección

# Recimos los datos para después pasarlo a la db


def put_todo(user_id, description):
    todos_collection_ref = db.collection(
        'users').document(user_id).collection('todos')
    # Datazo: para crear un documento y no poner atención al id es con add, de lo contrario usamos set como en la línea 19
    todos_collection_ref.add({
        'description': description,
        'done': False,
        'creation': datetime.now()
    })


def delete_todo(user_id, todo_id):
    #todo_ref = db.collection('users').document(user_id).collection('todos').document(todo_id)
    todo_ref = _get_ref(user_id, 'todo', todo_id)
    todo_ref.delete()


def update_todo(user_id, todo_id, done):
    todo_done = not bool(done)
    todo_ref = _get_ref(user_id, 'todos', todo_id)
    todo_ref.update({'done': todo_done})

# Switch para accceso a colección de primer segundo nivel


def _get_ref(user_id, collection, document_id):
    return db.document(f'users/{user_id}/{collection}/{document_id}')


def put_visit(user_id, visit_date, visitor, hashed_fields):
    visits_collection_ref = db.collection(
        'users').document(user_id).collection('visits')
    visits_collection_ref.add({
        'date': visit_date,
        'visitor': visitor,
        'hash': hashed_fields,
        'locked': False
    })


def get_visits(user_id):
    return db.collection('users').document(user_id).collection('visits').get()


def delete_visit(user_id, visit_id):
    visit_ref = _get_ref(user_id, 'visits', visit_id)
    visit_ref.delete()
