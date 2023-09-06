import requests
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
root = tk.Tk()

canvas1 = tk.Canvas(root, width=700, height=700)
canvas1.pack()

def uploadInventario():
    # Selección del path del archivo
    file_path = filedialog.askopenfilename()
    if file_path == '':
        exit()
    df = pd.read_excel(file_path)
    url = 'http://127.0.0.1:8080/producto/drop-all'
    x = requests.post(url)
    url = 'http://127.0.0.1:8080/producto/cargar'
    print(df.shape)
    max = df.shape[0]
    i = 1
    for ind in df.index:
        print(f'Cargando producto {df["Clave"][ind]}. \n{i} de {max}')
        myobj = {
                'nombre': df['Nombre'][ind],
                'precio': float(df['Precio'][ind]),
                'precio_esp': float(df['Precio_distribuidor'][ind]),
                'disponibles': int(df['Existencia'][ind]),
                'sku': df['Clave'][ind]
        }
        x = requests.post(url, json = myobj)
        i += 1
        print(x.text)

def cargar_datos():
    msg_box = tk.messagebox.askquestion('Subir archivo',
            '''Recuerda que al cargar un nuevo archivo se sobreescribira todo el inventario.''',
                                        icon='warning')
    if msg_box == 'yes':
        uploadInventario()
        root.destroy()

    else:
        tk.messagebox.showinfo('Cancelado', 'Se ha cancelado el proceso')
        exit()

def generar_reporte():
    pass

root.title('Sistema de Natural')
title = tk.Label(root, text="Escoge una opción del menú",font=("Arial", 25))
canvas1.create_window(350,50, window=title)

button_inventario = tk.Button(root, text='Cargar inventario', command=cargar_datos, bg='brown', fg='white')
canvas1.create_window(350, 150, window=button_inventario)

button_reporte = tk.Button(root, text='Generar reporte de ventas', command=generar_reporte, bg='brown', fg='white')
canvas1.create_window(350, 250, window=button_reporte)

root.mainloop()
root = tk.Tk()
root.withdraw()
