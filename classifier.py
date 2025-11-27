import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
import json
import os

class FoodClassifier:
    def __init__(self, custom_model_path=None):

        self.custom_model = custom_model_path is not None
        
        if self.custom_model:
            self.model = load_model(custom_model_path)
            
            class_indices_path = os.path.join(os.path.dirname(custom_model_path),'class_indices.json')
            with open(class_indices_path, 'r') as f:
                self.class_names = json.load(f)
            
            print(f"Custom model loaded from {custom_model_path}")
            print(f"Classes: {list(self.class_names.values())}")
        else:
            # pretrained model
            self.model = MobileNetV2(weights='imagenet')
            self.class_names = None
            print("MobileNetV2 model loaded successfully.")
    
    def preprocess_image(self, img_path):

        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        return img_array
    
    
    def classify(self, img_path, top_k=3):

        img_array = self.preprocess_image(img_path)
        predictions = self.model.predict(img_array)[0]
        
        if self.custom_model:
            # custom model - return top K predictions
            top_indices = predictions.argsort()[-top_k:][::-1]
            results = []
            for idx in top_indices:
                class_name = self.class_names[str(idx)]
                prob = predictions[idx]
                results.append((class_name, prob))
            return results
        else:
            # image net uses decode predictions
            decoded = decode_predictions(np.expand_dims(predictions, axis=0), top=top_k)[0]
            return decoded
    
    
    def get_food_name(self, img_path):

        predictions = self.classify(img_path, top_k=1)
        
        if self.custom_model:
            class_name = predictions[0][0]
        else:
            class_name = predictions[0][1]
        
        return class_name
