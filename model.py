import os
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image

# Load the trained model
model = load_model("plant_disease_model.h5")

# Replace with your dataset folder names in proper order
class_labels = sorted(os.listdir("C:/Users/LENOVO/Documents/chhaku ML/PlantVillage"))



def predict_disease(img: Image.Image) -> str:
    img = img.resize((224,224))
    img_array = np.array(img)/255.0
    prediction = model.predict(np.expand_dims(img_array, axis=0))
    return class_labels[np.argmax(prediction)]
