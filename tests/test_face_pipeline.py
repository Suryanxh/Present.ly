import numpy as np

import src.pipeline.face_pipeline as face_pipeline


def test_predict_attendance_reports_face_count_not_embedding_length(monkeypatch):
    monkeypatch.setattr(face_pipeline, "get_face_embeddings", lambda image: [
        np.array([1.0, 2.0, 3.0]),
        np.array([4.0, 5.0, 6.0]),
    ])
    monkeypatch.setattr(face_pipeline, "get_trained_model", lambda: None)

    _, _, num_faces = face_pipeline.predict_attendance(np.zeros((10, 10, 3), dtype=np.uint8))

    assert num_faces == 2
