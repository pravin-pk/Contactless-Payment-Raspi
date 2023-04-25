import requests
import json
import numpy as np
import cv2

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./contactless-payment.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def registerPalm():
	imageName = 'ROI.jpg'
	image = cv2.imread(f'./{imageName}', 0)

	image = image.reshape(-1,150,150,1)
	url = 'http://127.0.0.1:8888/register'

	data = json.dumps({'image': image.tolist()})
	headers = {'content-type': 'application/json'}
	r = requests.post(url, data=data, headers=headers)

	return json.loads(r.text)

def checkPalm():
	imageName = 'ROI.jpg'
	image = cv2.imread(f'./{imageName}', 0)

	image = image.reshape(-1,150,150,1)
	url = 'http://127.0.0.1:8888/match'

	data = json.dumps({'image': image.tolist()})
	headers = {'content-type': 'application/json'}
	r = requests.post(url, data=data, headers=headers)

	uniqueId = json.loads(r.text)['uniqueId']

	amount = db.collection('users').document(uniqueId).get().to_dict()['wallet']
	db.collection('users').document(uniqueId).update({'wallet': amount-100})
	db.collection('users').document(uniqueId).collection("transactions").add({'amount': 100, 'timestamp': firestore.SERVER_TIMESTAMP, 'type': 'debit'})
