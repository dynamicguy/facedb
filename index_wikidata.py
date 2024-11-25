from urllib.parse import urlparse
import requests
from elasticsearch import Elasticsearch
from deepface import DeepFace
from retinaface import RetinaFace
import cv2 as cv
from uuid import uuid4

from wiki_data_query_results import WikiDataQueryResults


def download_file(url, save_path):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
    }
    try:
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()  # Raise an exception for HTTP errors
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"File downloaded successfully: {save_path}")
        return save_path
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the file: {e}")
        return None


def extract_filename(url):
    parsed_url = urlparse(url)
    return parsed_url.path.split('/')[-1]


es = Elasticsearch(hosts=['http://localhost:9200'], http_auth=('elastic', 'DkIed99SCb'))

WDT_QUERY = """
SELECT DISTINCT ?person ?personLabel ?personDescription ?sitelinks ?genderLabel ?dob ?birthPlaceLabel ?coords ?image
WHERE {
    ?person wdt:P31 wd:Q5;            # Any instance of a human
          wdt:P19/wdt:P131* wd:Q60; # Who was born in any value (eg. a hospital)
          wikibase:sitelinks ?sitelinks.        
          ?person wdt:P21 ?gender.
          ?person wdt:P569 ?dob.
          ?person wdt:P106 ?occupation.
          ?person wdt:P551 ?residence.
          ?person wdt:P19 ?birthPlace.
          ?birthPlace wdt:P625 ?coords.
          ?person wdt:P18 ?image.
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
}
ORDER BY DESC(?sitelinks)
LIMIT 1000
"""

model_name = 'Facenet512'
target_size = (160, 160)
embedding_size = 512

mapping = {
    "mappings": {
        "properties": {
            "id": {"type": "keyword"},
            "title_vector": {
                "type": "dense_vector",
                "dims": embedding_size
            },
            "title_name": {"type": "keyword"},
            "description": {"type": "keyword"},
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
        }
    }
}

try:
    es.indices.create(index="facedb", body=mapping)
except:
    pass

data_extracter = WikiDataQueryResults(WDT_QUERY)
df = data_extracter.load_as_dataframe()

for index, row in df.iterrows():
    fname = extract_filename(row['image'])
    print(row['personLabel'], fname, row['image'])
    img_path = 'public/data/' + fname
    download_file(row['image'], img_path)

    try:
        embedding_objs = DeepFace.represent(img_path=img_path, model_name=model_name, detector_backend='retinaface', align=True)
        embedding = embedding_objs[0]["embedding"]

        target_faces = RetinaFace.extract_faces(img_path = img_path, align = True)
        target_img = target_faces[0]
        cv.imwrite(img_path + ".face.jpg", target_img[...,::-1])

        objs = DeepFace.analyze(
            img_path = img_path,
            actions = ['age', 'gender', 'race', 'emotion'],
            detector_backend='retinaface',
        )

        doc = {
            "id": uuid4().hex,
            "title_vector": embedding,
            "title_name": row['personLabel'],
            'description': row['personDescription'],
            'img_path': img_path,
            'gender': row['genderLabel'],
            'dob': row['dob'],
            'birth_place': row['birthPlaceLabel'],
            'image_url': row['image'],
            'face_path': img_path + ".face.jpg",
            'identified_age': objs[0].get('age'),
            'identified_gender': objs[0].get('dominant_gender'),
            'identified_race': objs[0].get('dominant_race'),
            'identified_emotion': objs[0].get('dominant_emotion'),
        }
        print('indexing', row['personLabel'])
        es.create("facedb", id=index, body=doc)
    except:
        pass
