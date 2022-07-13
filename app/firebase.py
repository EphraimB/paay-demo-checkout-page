import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('app/paay-86a57-f0fb4772421c.json')
firebase_admin.initialize_app(cred)

db = firestore.client()