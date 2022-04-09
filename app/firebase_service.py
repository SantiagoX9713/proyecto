import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Login y comunicación con nuestro proyecto de GCP
credential = credentials.ApplicationDefault()
firebase_admin .initialize_app(credential)

# Instancia de Firestore
db = firestore.client()

#Primera función para obtener colecciones de Firestore

def get_users():
    return db.collection('users').get()