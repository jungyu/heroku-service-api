import os
import firebase_admin
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app

app= Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('line-bot-ecommerce-fe1fdd0257c4.json')
default_app = initialize_app(cred)
db = firestore.client()

@app.route('/')
def index():
  return "<h1>Welcome to Line Bot Ecommerce API</h1>"

@app.route('/add/<collection_name>', methods=['POST'])
def create(collection_name=None):
    """
        create() : Add document to Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    try:
        id = request.json['id']
        collection_ref = db.collection(collection_name)
        collection_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

@app.route('/list/<collection_name>', methods=['GET'])
def read(collection_name=None):
    """
        read() : Fetches documents from Firestore collection as JSON.
        todo : Return document that matches query ID.
        all_todos : Return all documents.
    """
    try:
        # Check if ID was passed to URL query
        id = request.args.get('id')
        collection_ref = db.collection(collection_name)
        if id:
            collection = collection_ref.document(id).get()
            return jsonify(collection.to_dict()), 200
        else:
            all_collections = [doc.to_dict() for doc in collection_ref.stream()]
            return jsonify(all_collections), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

@app.route('/update/<collection_name>', methods=['POST', 'PUT'])
def update(collection_name=None):
    """
        update() : Update document in Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        id = request.json['id']
        collection_ref = db.collection(collection_name)
        collection_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

@app.route('/delete/<collection_name>', methods=['GET', 'DELETE'])
def delete(collection_name=None):
    """
        delete() : Delete a document from Firestore collection.
    """
    try:
        # Check for ID in URL query
        id = request.args.get('id')
        collection_ref = db.collection(collection_name)
        collection_ref.document(id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"