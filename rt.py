from deepface import DeepFace

DeepFace.stream(db_path="dataset/db", enable_face_analysis=True, model_name="ArcFace", distance_metric="cosine", time_threshold=1)