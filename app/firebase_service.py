import firebase_admin
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
    user_ref.set({'password': user_data.password})

# Para obtener los todos del usuario user_id
def get_todos(user_id):
    return db.collection('users').document(user_id).collection('todos').get()
# collection() para saber a que coleccion entrar y después obtener
# los documentos todos y con get() traemos toda la colección

# Recimos los datos para después pasarlo a la db
def put_todo(user_id, description):
    todos_collection_ref = db.collection('users').document(user_id).collection('todos')
    # Datazo: para crear un documento y no poner atención al id es con add, de lo contrario usamos set como en la línea 19
    todos_collection_ref.add({'description': description, 'done': False})


def delete_todo(user_id, todo_id):
    #todo_ref = db.collection('users').document(user_id).collection('todos').document(todo_id)
    todo_ref = db.document('users/{}/todos/{}'.format(user_id, todo_id))
    todo_ref.delete()