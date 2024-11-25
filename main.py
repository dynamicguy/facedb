from typing import Union
from deepface import DeepFace
from elasticsearch import Elasticsearch
from fastapi import FastAPI
import time
from fastapi import File, UploadFile, HTTPException

app = FastAPI()

ES = Elasticsearch(hosts=['http://localhost:9200'], http_auth=('elastic', 'DkIed99SCb'))
ES_INDEX = 'facedb'
MODEL_NAME = 'Facenet512'

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
def upload(file: UploadFile = File(...)):
    print('FILE', file)
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
            'total': res['hits']['total']['value'],
            'q': {
                'identified_age': objs[0].get('age'),
                'identified_gender': objs[0].get('dominant_gender'),
                'identified_race': objs[0].get('dominant_race'),
                'identified_emotion': objs[0].get('dominant_emotion'),
            },
            'items': items
        }
