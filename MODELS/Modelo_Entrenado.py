import os
import numpy as np
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from sklearn.model_selection import train_test_split

# Cargar MNIST
(x_train_mnist, y_train_mnist), (x_test_mnist, y_test_mnist) = mnist.load_data()

# Normalizar MNIST
x_train_mnist = x_train_mnist / 255.0
x_test_mnist = x_test_mnist / 255.0

# Agregar canal de color (escala de grises)
x_train_mnist = x_train_mnist.reshape((-1, 28, 28, 1))
x_test_mnist = x_test_mnist.reshape((-1, 28, 28, 1))

# One-hot encoding de etiquetas
y_train_mnist = to_categorical(y_train_mnist, 10)
y_test_mnist = to_categorical(y_test_mnist, 10)

# Cargar imágenes personalizadas
custom_images_dir = "digitos_guardados"
custom_images = []
custom_labels= []

for filename in os.listdir(custom_images_dir):
    if filename.endswith(".png"):
        label_str = filename.split("_")[1].split(".")[0]  # numero_X.png
        try:
            label = int(label_str)
            img_path = os.path.join(custom_images_dir, filename)
            img = load_img(img_path, color_mode='grayscale', target_size=(28, 28))
            img_array = img_to_array(img)
            img_array = 255 - img_array  # Invertir fondo negro, número blanco
            img_array = img_array / 255.0
            custom_images.append(img_array)
            custom_labels.append(label)
        except ValueError:
            print(f"❌ Archivo ignorado: {filename}")

if not custom_images:
    print("⚠️ No se encontraron imágenes personalizadas. ¿Guardaste alguna en 'digitos_guardados'?")
    exit()

x_custom = np.array(custom_images)
x_custom = x_custom.reshape((-1, 28, 28, 1))
y_custom = to_categorical(custom_labels, 10)

# Unir MNIST + imágenes personalizadas
x_total = np.concatenate((x_train_mnist, x_custom), axis=0)
y_total = np.concatenate((y_train_mnist, y_custom), axis=0)

# Dividir en entrenamiento y validación
x_train, x_val, y_train, y_val = train_test_split(x_total, y_total, test_size=0.1, random_state=42)

# Crear modelo CNN
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(10, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Entrenar
print("🧠 Entrenando modelo con MNIST + dibujos personalizados...")
model.fit(x_train, y_train, epochs=5, validation_data=(x_val, y_val), batch_size=32)

# Guardar modelo
model.save("MODELS/Modelo_Entrenado.h5")
print("✅ Modelo guardado como MODELS/Modelo_Entrenado.h5")
