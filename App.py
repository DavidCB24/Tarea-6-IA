from flask import Flask, render_template, request, redirect, url_for
import cv2
import numpy as np
import pytesseract
from PIL import Image
import os
from num2words import num2words
import math
import mysql.connector

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configura tu ruta de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Función para calcular factorial o aproximarlo
def calcular_factorial(numero):
    if numero <= 1000:
        return math.factorial(numero)
    else:
        # Aproximación usando fórmula de Stirling
        stirling_approx = 0.5 * math.log10(2 * math.pi * numero) + numero * math.log10(numero / math.e)
        return f"Aproximadamente {stirling_approx:.2f} dígitos en el factorial"

# Función para insertar en la base de datos
def insertar_en_bd(numero, factorial):
    try:
        conexion = mysql.connector.connect(
            host="www.server.daossystem.pro",
            port=3301,
            user="usr_ia_lf_2025",
            password="5sr_31_lf_2025",
            database="bd_ia_lf_2025"
        )
        cursor = conexion.cursor()
        sql = "INSERT INTO segundo_parcial (valor, factorial, nombre_estudiante) VALUES (%s, %s, %s)"
        valores = (str(numero), str(factorial), "Wilmi Cabrera")  # <--- pon aquí tu nombre real
        cursor.execute(sql, valores)
        conexion.commit()
        cursor.close()
        conexion.close()
        print("✅ Datos insertados correctamente en la base de datos.")
    except Exception as e:
        print(f"❌ Error al insertar en la base de datos: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def procesar():
    if 'imagen' not in request.files:
        return redirect(url_for('index'))

    archivo = request.files['imagen']
    if archivo.filename == '':
        return redirect(url_for('index'))

    ruta = os.path.join(UPLOAD_FOLDER, archivo.filename)
    archivo.save(ruta)

    img = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
    _, img_bin = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

    texto = pytesseract.image_to_string(img_bin, config='--psm 6 digits')
    numero_detectado = ''.join(filter(str.isdigit, texto))

    if numero_detectado == '':
        return render_template('resultado.html', numero_detectado="No se detectó número.", numero_letras='-', factorial='-')

    if len(numero_detectado) > 6:
        return render_template('resultado.html', numero_detectado="Número demasiado grande.", numero_letras='-', factorial='-')

    numero = int(numero_detectado)

    try:
        numero_letras = num2words(numero, lang='es')
    except (OverflowError, ValueError):
        numero_letras = "Número muy grande para convertir"

    factorial_resultado = calcular_factorial(numero)

    # Insertar en la base de datos
    insertar_en_bd(numero, factorial_resultado)

    return render_template('resultado.html', numero_detectado=numero, numero_letras=numero_letras, factorial=factorial_resultado)

if __name__ == '__main__':
    app.run(debug=True)
