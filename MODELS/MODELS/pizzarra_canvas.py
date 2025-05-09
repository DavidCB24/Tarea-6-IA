import tkinter as tk
from PIL import Image, ImageDraw
import os
from tkinter import simpledialog, messagebox

# Crear carpeta para guardar imágenes si no existe
output_dir = "digitos_guardados"
os.makedirs(output_dir, exist_ok=True)

# Crear la ventana
ventana = tk.Tk()
ventana.title("Pizarrón para Números")

# Crear canvas negro de 280x280
canvas_ancho, canvas_alto = 280, 280
canvas = tk.Canvas(ventana, width=canvas_ancho, height=canvas_alto, bg="black")
canvas.pack()

# Crear una imagen en negro donde se dibujará en blanco
imagen = Image.new("L", (canvas_ancho, canvas_alto), color=0)  # fondo negro
draw = ImageDraw.Draw(imagen)

def dibujar(event):
    x, y = event.x, event.y
    r = 8
    canvas.create_oval(x - r, y - r, x + r, y + r, fill="white", outline="white")
    draw.ellipse([x - r, y - r, x + r, y + r], fill=255)  # blanco (255) en imagen

def guardar_imagen():
    numero = simpledialog.askstring("Guardar número", "¿Qué número dibujaste?")
    if numero is None or not numero.isdigit() or not (0 <= int(numero) <= 9):
        messagebox.showerror("Error", "Debes ingresar un número del 0 al 9.")
        return

    archivos_existentes = [f for f in os.listdir(output_dir) if f.startswith(f"{numero}_")]
    siguiente_numero = len(archivos_existentes)
    nombre_archivo = f"{numero}_{siguiente_numero}.png"
    ruta = os.path.join(output_dir, nombre_archivo)

    imagen_redimensionada = imagen.resize((28, 28))
    imagen_redimensionada.save(ruta)
    print(f"✅ Imagen guardada como: {ruta}")
    limpiar_canvas()

def limpiar_canvas():
    canvas.delete("all")
    draw.rectangle([0, 0, canvas_ancho, canvas_alto], fill=0)  # negro

# Eventos
canvas.bind("<B1-Motion>", dibujar)

# Botones
boton_guardar = tk.Button(ventana, text="Guardar", command=guardar_imagen)
boton_guardar.pack(side=tk.LEFT, padx=10)

boton_limpiar = tk.Button(ventana, text="Limpiar", command=limpiar_canvas)
boton_limpiar.pack(side=tk.RIGHT, padx=10)

ventana.mainloop()
