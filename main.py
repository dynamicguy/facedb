from typing import Union
from uuid import uuid4

from deepface import DeepFace
from elasticsearch import Elasticsearch
from fastapi import FastAPI
import time
from fastapi import File, UploadFile, HTTPException
from pydantic import BaseModel
from retinaface import RetinaFace
import cv2 as cv
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/public", StaticFiles(directory="public"), name="public")

ES = Elasticsearch(hosts=['http://localhost:9200'], http_auth=('elastic', 'DkIed99SCb'))
ES_INDEX = 'facedb'
MODEL_NAME = 'Facenet512'


class Item(BaseModel):
    name: str
    description: str | None = None
    gender: str | None = None
    dob: str | None = None
    birth_place: str | None = None
    img_path: str | None = None
    identified_age: int | None = None
    identified_gender: str | None = None
    identified_race: str | None = None
    identified_emotion: str | None = None


@app.get("/api/items")
def read_root(limit: Union[int, None] = 12):
    query = {
        "size": limit,
        "query": {
            "match_all": {}
        }
    }
    res = ES.search(index=ES_INDEX, body=query)
    items = []
    for i in res["hits"]["hits"]:
        items.append({
            'id': i["_source"]["id"],
            'name': i["_source"]["title_name"],
            'description': i["_source"]["description"],
            "img_path": i["_source"]['img_path'],
            "gender": i["_source"]['gender'],
            "dob": i["_source"]['dob'],
            "birth_place": i["_source"]['birth_place'],
            "image_url": i["_source"]['image_url'],
            "face_path": i["_source"]['face_path'],
            "identified_age": i["_source"]['identified_age'],
            "identified_gender": i["_source"]['identified_gender'],
            "identified_race": i["_source"]['identified_race'],
            "identified_emotion": i["_source"]['identified_emotion']
        })

    return items


@app.get("/api/items/{item_id}")
def read_item(item_id: str, q: Union[str, None] = None):
    query = {
        "size": 1,
        "query": {
            "match": {"id": item_id}
        }
    }
    res = ES.search(index=ES_INDEX, body=query)
    i = res["hits"]["hits"][0]
    return {
        'id': i["_source"]["id"],
        'name': i["_source"]["title_name"],
        'description': i["_source"]["description"],
        "img_path": i["_source"]['img_path'],
        "gender": i["_source"]['gender'],
        "dob": i["_source"]['dob'],
        "birth_place": i["_source"]['birth_place'],
        "image_url": i["_source"]['image_url'],
        "face_path": i["_source"]['face_path'],
        "identified_age": i["_source"]['identified_age'],
        "identified_gender": i["_source"]['identified_gender'],
        "identified_race": i["_source"]['identified_race'],
        "identified_emotion": i["_source"]['identified_emotion']
    }


@app.post("/api/search")
def search(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        upload_path = 'public/uploads/' + file.filename
        with open(upload_path, 'wb') as f:
            f.write(contents)
    except Exception:
        raise HTTPException(status_code=500, detail='Something went wrong')
    finally:
        file.file.close()
        embedding_objs = DeepFace.represent(img_path=upload_path,
                                            model_name=MODEL_NAME,
                                            detector_backend='retinaface',
                                            align=True
                                            )
        target_embedding = embedding_objs[0]["embedding"]

        objs = DeepFace.analyze(
            img_path=upload_path,
            actions=['age', 'gender', 'race', 'emotion'],
            detector_backend='retinaface',
        )

        query = {
            "size": 12,
            "query": {
                "script_score": {
                    "query": {
                        "match": {"identified_gender": objs[0].get('dominant_gender')},
                        # "match_all": {},
                    },
                    "script": {
                        "source": "cosineSimilarity(params.queryVector, 'title_vector') + 1.0",
                        # "source": "1 / (1 + l2norm(params.queryVector, 'title_vector'))", #euclidean distance
                        "params": {
                            "queryVector": list(target_embedding)
                        }
                    }
                }
            }
        }
        tic = time.time()
        res = ES.search(index=ES_INDEX, body=query)
        toc = time.time()
        print(toc - tic, " seconds")
        items = []
        for i in res["hits"]["hits"]:
            items.append({
                'id': i["_source"]["id"],
                'name': i["_source"]["title_name"],
                'description': i["_source"]["description"],
                "img_path": i["_source"]['img_path'],
                "gender": i["_source"]['gender'],
                "dob": i["_source"]['dob'],
                "birth_place": i["_source"]['birth_place'],
                "image_url": i["_source"]['image_url'],
                "face_path": i["_source"]['face_path'],
                "identified_age": i["_source"]['identified_age'],
                "identified_gender": i["_source"]['identified_gender'],
                "identified_race": i["_source"]['identified_race'],
                "identified_emotion": i["_source"]['identified_emotion'],
                "score": i["_score"],
            })

        return {
            'took': res['took'],
            'total': res['hits']['total']['value'],
            'q': {
                'identified_age': objs[0].get('age'),
                'identified_gender': objs[0].get('dominant_gender'),
                'identified_race': objs[0].get('dominant_race'),
                'identified_emotion': objs[0].get('dominant_emotion'),
            },
            'items': items
        }


@app.post("/api/analyze")
def analyze(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        upload_path = 'public/uploads/' + file.filename
        with open(upload_path, 'wb') as f:
            f.write(contents)
    except Exception:
        raise HTTPException(status_code=500, detail='Something went wrong')
    finally:
        file.file.close()
        objs = DeepFace.analyze(
            img_path=upload_path,
            actions=['age', 'gender', 'race', 'emotion'],
            detector_backend='retinaface',
        )

        return {
            'img_path': upload_path,
            'identified_age': objs[0].get('age'),
            'identified_gender': objs[0].get('dominant_gender'),
            'identified_race': objs[0].get('dominant_race'),
            'identified_emotion': objs[0].get('dominant_emotion'),
        }


@app.post("/api/add")
async def create_item(item: Item):
    print(item.dob)
    embedding_objs = DeepFace.represent(img_path=item.img_path, model_name=MODEL_NAME, detector_backend='retinaface',
                                        align=True)
    embedding = embedding_objs[0]["embedding"]

    target_faces = RetinaFace.extract_faces(img_path=item.img_path, align=True)
    target_img = target_faces[0]
    cv.imwrite(item.img_path + ".face.jpg", target_img[..., ::-1])
    ID = uuid4().hex
    doc = {
        "id": ID,
        "title_vector": embedding,
        "title_name": item.name,
        'description': item.description,
        'img_path': item.img_path,
        'gender': item.gender,
        'dob': item.dob,
        'birth_place': item.birth_place,
        'image_url': 'http://localhost:8000/' + item.img_path,
        'face_path': item.img_path + ".face.jpg",
        'identified_age': item.identified_age,
        'identified_gender': item.identified_gender,
        'identified_race': item.identified_race,
        'identified_emotion': item.identified_emotion,
    }
    ES.create(ES_INDEX, id=ID, body=doc)
    return doc
