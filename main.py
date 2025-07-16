from typing import Union
from uuid import uuid4
import os
from deepface import DeepFace
from elasticsearch import Elasticsearch
import time
from retinaface import RetinaFace
import cv2 as cv
from fastapi.staticfiles import StaticFiles
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    role: str | None = "user"


class Token(BaseModel):
    access_token: str
    token_type: str
    user: User


class UserDTO(BaseModel):
    username: str
    password: str
    email: str | None = None
    full_name: str | None = None


class UserInDB(User):
    hashed_password: str
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    role: str | None = "user"


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


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

app = FastAPI()

app.mount("/public", StaticFiles(directory="public"), name="public")

ES = Elasticsearch(hosts=["http://localhost:9200"], http_auth=("elastic", "DkIed99SCb"))
ES_INDEX = os.getenv("ES_INDEX", "facedb")
MODEL_NAME = os.getenv("MODEL_NAME", "Facenet512")
SECRET_KEY = os.getenv(
    "SECRET_KEY", "17dfb1a5c43144b0f041be2c14289aab236de064db1d59d945abfb206dba0d08"
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_users_from_db():
    res = ES.search(index="users", body={})
    items = []
    for i in res["hits"]["hits"]:
        items.append(
            {
                "id": i["_source"]["id"],
                "hashed_password": i["_source"]["hashed_password"],
                "username": i["_source"]["username"],
                "email": i["_source"]["email"],
                "full_name": i["_source"]["full_name"],
                "disabled": i["_source"]["disabled"],
                "role": i["_source"]["role"],
            }
        )
    return items


DB_USERS = get_users_from_db()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
    for user in DB_USERS:
        if user.get("username") == username:
            return user
    return None


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.get("hashed_password")):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.get("disabled"):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/api/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.get("username")}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer", user=user)


@app.get("/api/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@app.get("/api/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.get("username")}]


@app.post("/api/users/register")
async def create_user(user: UserDTO):
    ID = uuid4().hex
    doc = {
        "id": ID,
        "username": user.username,
        "hashed_password": get_password_hash(user.password),
        "email": user.email,
        "full_name": user.full_name,
        "role": "user",
        "disabled": True,
    }
    ES.create("users", id=ID, body=doc)
    return doc


@app.get("/api/items")
def get_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
    limit: Union[int, None] = 12,
):
    query = {"size": limit, "query": {"match_all": {}}}
    res = ES.search(index=ES_INDEX, body=query)
    items = []
    for i in res["hits"]["hits"]:
        items.append(
            {
                "id": i["_source"]["id"],
                "name": i["_source"]["title_name"],
                "description": i["_source"]["description"],
                "img_path": i["_source"]["img_path"],
                "gender": i["_source"]["gender"],
                "dob": i["_source"]["dob"],
                "birth_place": i["_source"]["birth_place"],
                "image_url": i["_source"]["image_url"],
                "face_path": i["_source"]["face_path"],
                "identified_age": i["_source"]["identified_age"],
                "identified_gender": i["_source"]["identified_gender"],
                "identified_race": i["_source"]["identified_race"],
                "identified_emotion": i["_source"]["identified_emotion"],
                "username": i["_source"]["username"],
                "created_at": i["_source"]["created_at"],
            }
        )

    return items


@app.get("/api/items/{item_id}")
def read_item(
    current_user: Annotated[User, Depends(get_current_active_user)],
    item_id: str,
    q: Union[str, None] = None,
):
    query = {"size": 1, "query": {"match": {"id": item_id}}}
    res = ES.search(index=ES_INDEX, body=query)
    i = res["hits"]["hits"][0]
    return {
        "id": i["_source"]["id"],
        "name": i["_source"]["title_name"],
        "description": i["_source"]["description"],
        "img_path": i["_source"]["img_path"],
        "gender": i["_source"]["gender"],
        "dob": i["_source"]["dob"],
        "birth_place": i["_source"]["birth_place"],
        "image_url": i["_source"]["image_url"],
        "face_path": i["_source"]["face_path"],
        "identified_age": i["_source"]["identified_age"],
        "identified_gender": i["_source"]["identified_gender"],
        "identified_race": i["_source"]["identified_race"],
        "identified_emotion": i["_source"]["identified_emotion"],
    }


@app.post("/api/search")
def search(
    current_user: Annotated[User, Depends(get_current_active_user)],
    file: UploadFile = File(...),
):
    try:
        contents = file.file.read()
        if not os.path.exists("public/uploads/" + current_user.get("username")):
            os.mkdir("public/uploads/" + current_user.get("username"))

        upload_path = (
            "public/uploads/" + current_user.get("username") + "/" + file.filename
        )
        with open(upload_path, "wb") as f:
            f.write(contents)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
    finally:
        file.file.close()
        embedding_objs = DeepFace.represent(
            img_path=upload_path,
            model_name=MODEL_NAME,
            detector_backend="retinaface",
            align=True,
        )
        target_embedding = embedding_objs[0]["embedding"]

        objs = DeepFace.analyze(
            img_path=upload_path,
            actions=["age", "gender", "race", "emotion"],
            detector_backend="retinaface",
        )

        query = {
            "size": 12,
            "query": {
                "script_score": {
                    "query": {
                        "match": {"identified_gender": objs[0].get("dominant_gender")},
                        # "match_all": {},
                    },
                    "script": {
                        "source": "cosineSimilarity(params.queryVector, 'title_vector') + 1.0",
                        # "source": "1 / (1 + l2norm(params.queryVector, 'title_vector'))", #euclidean distance
                        "params": {"queryVector": list(target_embedding)},
                    },
                }
            },
        }
        tic = time.time()
        res = ES.search(index=ES_INDEX, body=query)
        toc = time.time()
        print(toc - tic, " seconds")
        items = []
        for i in res["hits"]["hits"]:
            items.append(
                {
                    "id": i["_source"]["id"],
                    "name": i["_source"]["title_name"],
                    "description": i["_source"]["description"],
                    "img_path": i["_source"]["img_path"],
                    "gender": i["_source"]["gender"],
                    "dob": i["_source"]["dob"],
                    "birth_place": i["_source"]["birth_place"],
                    "image_url": i["_source"]["image_url"],
                    "face_path": i["_source"]["face_path"],
                    "identified_age": i["_source"]["identified_age"],
                    "identified_gender": i["_source"]["identified_gender"],
                    "identified_race": i["_source"]["identified_race"],
                    "identified_emotion": i["_source"]["identified_emotion"],
                    "score": i["_score"],
                }
            )

        return {
            "took": res["took"],
            "total": res["hits"]["total"]["value"],
            "q": {
                "identified_age": objs[0].get("age"),
                "identified_gender": objs[0].get("dominant_gender"),
                "identified_race": objs[0].get("dominant_race"),
                "identified_emotion": objs[0].get("dominant_emotion"),
            },
            "items": items,
        }


@app.post("/api/analyze")
def analyze(
    current_user: Annotated[User, Depends(get_current_active_user)],
    file: UploadFile = File(...),
):
    try:
        if not os.path.exists("public/uploads/" + current_user.get("username")):
            os.mkdir("public/uploads/" + current_user.get("username"))
        contents = file.file.read()
        upload_path = (
            "public/uploads/" + current_user.get("username") + "/" + file.filename
        )
        with open(upload_path, "wb") as f:
            f.write(contents)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
    finally:
        file.file.close()
        objs = DeepFace.analyze(
            img_path=upload_path,
            actions=["age", "gender", "race", "emotion"],
            detector_backend="retinaface",
        )

        return {
            "img_path": upload_path,
            "identified_age": objs[0].get("age"),
            "identified_gender": objs[0].get("dominant_gender"),
            "identified_race": objs[0].get("dominant_race"),
            "identified_emotion": objs[0].get("dominant_emotion"),
        }


@app.post("/api/add")
async def create_item(
    current_user: Annotated[User, Depends(get_current_active_user)], item: Item
):
    embedding_objs = DeepFace.represent(
        img_path=item.img_path,
        model_name=MODEL_NAME,
        detector_backend="retinaface",
        align=True,
    )
    embedding = embedding_objs[0]["embedding"]

    target_faces = RetinaFace.extract_faces(img_path=item.img_path, align=True)
    target_img = target_faces[0]
    cv.imwrite(item.img_path + ".face.jpg", target_img[..., ::-1])
    ID = uuid4().hex
    doc = {
        "id": ID,
        "title_vector": embedding,
        "title_name": item.name,
        "description": item.description,
        "img_path": item.img_path,
        "gender": item.gender,
        "dob": item.dob,
        "birth_place": item.birth_place,
        "image_url": "http://localhost:8000/" + item.img_path,
        "face_path": item.img_path + ".face.jpg",
        "identified_age": item.identified_age,
        "identified_gender": item.identified_gender,
        "identified_race": item.identified_race,
        "identified_emotion": item.identified_emotion,
        "username": current_user.get("username"),
        "created_at": datetime.now(timezone.utc),
    }
    ES.create(ES_INDEX, id=ID, body=doc)
    return doc
