import tensorflow as tf
import numpy as np
import cv2
from fastapi import UploadFile

# Load pre-trained models
M1 = tf.keras.models.load_model("models/model_1.h5")
M2 = tf.keras.models.load_model("models/model_2.h5")
M3 = tf.keras.models.load_model("models/model_3.h5")
M4 = tf.keras.models.load_model("models/model_4.h5")

# Class labels
LABELS_M3 = ["Mildew", "Brown", "Yellow", "Stem"]
LABELS_M4 = ["Fusarium", "Loose Smut", "Septoria", "Common Root Rot"]

def preprocess_image(file: UploadFile):
    contents = file.file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (224, 224)) / 255.0
    return np.expand_dims(img, axis=0)

def classify_image(file: UploadFile):
    image = preprocess_image(file)

    # Step 1: Model M1 - Healthy or Not
    result_m1 = M1.predict(image)
    if result_m1[0][0] > 0.5:
        return {"class": "Healthy", "accuracy": float(result_m1[0][0]) * 100}

    # Step 2: Model M2 - Rust or Others
    result_m2 = M2.predict(image)
    if result_m2[0][0] > 0.5:
        result_m3 = M3.predict(image)
        label = LABELS_M3[np.argmax(result_m3)]
        return {"class": label, "accuracy": float(max(result_m3[0])) * 100}
    else:
        result_m4 = M4.predict(image)
        label = LABELS_M4[np.argmax(result_m4)]
        return {"class": label, "accuracy": float(max(result_m4[0])) * 100}
