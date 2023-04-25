import requests
import json
import numpy as np
import cv2

def connect():
	imageName = 'ROI.jpg'
	image = cv2.imread(f'./{imageName}', 0)

	image = image.reshape(-1,150,150,1)
	url = 'http://127.0.0.1:8888/register'

	data = json.dumps({'image': image.tolist()})
	headers = {'content-type': 'application/json'}
	r = requests.post(url, data=data, headers=headers)

	return json.loads(r.text)
