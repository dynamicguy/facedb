from elasticsearch import Elasticsearch
from deepface import DeepFace
import matplotlib.pyplot as plt
from retinaface import RetinaFace
import os
import time
import glob
from faker import Faker
from uuid import uuid4
from datetime import datetime
import cv2 as cv

model_name = 'Facenet512'
index_name = 'suspects2'
target_size = (160, 160)
embedding_size = 512

es = Elasticsearch(hosts=['http://localhost:9200'], http_auth=('elastic', 'DkIed99SCb'))

es.indices.delete(index=index_name, ignore=[400, 404])

mapping = {
    "mappings": {
        "properties": {
            "id": {"type": "keyword"},
            "face_vector": {
                "type": "dense_vector",
                "dims": embedding_size
            },
            "name": {"type": "text"},
            "bio": {"type": "text"},
            "img_path": {"type": "keyword"},
            "gender": {"type": "keyword"},
            "dob": {"type": "date"},
            "birth_place": {"type": "keyword"},
            "image_url": {"type": "keyword"},
            "face_path": {"type": "keyword"},
            "identified_age": {"type": "keyword"},
            "identified_gender": {"type": "keyword"},
            "identified_race": {"type": "keyword"},
            "identified_emotion": {"type": "keyword"},
            "username": {"type": "keyword"},
            "created_at": {"type": "date"}
        }
    }
}

es.indices.create(index=index_name, body=mapping)

dir_path = "public/suspects2/*.*"
res = glob.glob(dir_path, recursive=True)
files = []
for item in res:
    if item.endswith('.jpg'):
        files.append(item)
print('total files:', len(files))

tic = time.time()
fake = Faker('bn_BD')

for img_path in files:
    print('Indexing', img_path, 'index', files.index(img_path)+1, 'of', len(files))
    try:
        embedding_objs = DeepFace.represent(img_path=img_path, model_name=model_name, detector_backend='retinaface', align=True)
        embedding = embedding_objs[0]["embedding"]

        target_faces = RetinaFace.extract_faces(img_path = img_path, align = True)
        target_img = target_faces[0]
        cv.imwrite(img_path + ".face.png", target_img[...,::-1])

        objs = DeepFace.analyze(
            img_path = img_path,
            actions = ['age', 'gender', 'race', 'emotion'],
            detector_backend='retinaface',
        )
        ID = uuid4().hex
        gender = objs[0].get('dominant_gender')
                
        if gender == 'Man':
            name = fake.name_male()
        else:
            name = fake.name_female()

        doc = {
            "id": ID,
            "face_vector": embedding,
            "name": name,
            'bio': fake.text(),
            'img_path': img_path,
            'gender': gender,
            'dob': datetime.strptime(fake.date_of_birth(tzinfo=None, minimum_age=objs[0].get('age'), maximum_age=objs[0].get('age')).isoformat(), '%Y-%m-%d'),
            'birth_place': fake.city(),
            'image_url': 'http://localhost:8000/' + img_path,
            'face_path': img_path + ".face.png",
            'identified_age': objs[0].get('age'),
            'identified_gender': objs[0].get('dominant_gender'),
            'identified_race': objs[0].get('dominant_race'),
            'identified_emotion': objs[0].get('dominant_emotion'),
            'username': 'ferdous',
            'created_at': datetime.now(),
        }    
        es.create(index=index_name, id=ID, body=doc)
    except:
        pass

toc = time.time()
print("indexing completed in ", toc-tic, " seconds")