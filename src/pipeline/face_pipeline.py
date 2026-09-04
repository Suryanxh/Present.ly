

import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students

# as it is heavy thus loaded once
@st.cache_resource
def load_dlib_model():
    detector = dlib.get_frontal_face_detector()


    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec

def get_face_embeddings(image_np):

    detector, sp, facerec = load_dlib_model()

    faces = detector(image_np, 1)

    encodings =[]

    for face in faces:
        shape = sp(image_np, face)

        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1)

        encodings.append(np.array(face_descriptor))
    return encodings

@st.cache_resource
def get_trained_model():
    X = []
    y = []

    student_db = get_all_students()

    if not student_db:
        return None

    for student in student_db:
        embedding = student.get('face_embedding')
        if embedding:
            X.append(np.array(embedding))
            y.append(student.get('student_id'))

    if len(X) == 0:
        return 0

    clf = SVC(kernel = 'linear', probability= True, class_weight='balanced')


    try:
        clf.fit(X, y)

    except ValueError:
        pass

    return {'clf' : clf, 'X' : X, 'y' : y}


def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)

def predict_attendance(class_image_np):
    encodings = get_face_embeddings(class_image_np)
    num_faces = len(encodings)

    detected_students = {}

    model_data = get_trained_model()

    if not model_data:
        return detected_students, [], num_faces

    X_train = model_data['X']
    y_train = model_data['y']

    all_students = sorted(list(set(y_train)))

    for encoding in encodings:
        distances = [np.linalg.norm(embedding - encoding) for embedding in X_train]
        closest_index = int(np.argmin(distances))
        predicted_id = int(y_train[closest_index])
        best_match_score = distances[closest_index]

        resemblence_threshold = 0.5

        if best_match_score <= resemblence_threshold:
            detected_students[predicted_id] = True

    return detected_students, all_students, num_faces