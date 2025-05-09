import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import os

# Cargar el modelo entrenado
model_path = os.path.join('MODELS', 'Modelo_Entrenado.h5')
model = load_model(model_path)

# Ruta de la imagen a predecir
image_path = os.path.join('MODELS','MODELS', 'Numero.jpg')

# Cargar y procesar la imagen
img = Image.open(image_path).convert('L')  # Convertir a escala de grises
img = img.resize((28, 28))                 # Redimensionar a 28x28
img_array = np.array(img) / 255.0          # Normalizar
img_array = img_array.reshape(1, 28, 28)   # Ajustar forma para el modelo

# Realizar predicción
prediction = model.predict(img_array)
predicted_digit = np.argmax(prediction)

print(f'El modelo predice que el dígito es: {predicted_digit}')
