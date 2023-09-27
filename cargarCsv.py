import json

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
                'precio': float(df['Precio_lista'][ind]),
                'disponibles': int(df['Existencia'][ind]),
                'descuento': df['Descuento'][ind] / (100),
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
    url = 'http://127.0.0.1:8080/venta/reporte'
    from tkinter.filedialog import asksaveasfile
    file_path = asksaveasfile(initialfile='Reporte.xlsx',
                              defaultextension=".xlsx", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])

    if file_path.name == '':
        exit()
    myobj = {
        "path": file_path.name
    }
    x = requests.post(url, json=myobj)
    exit()

def subir_distribuidores():
    file_path = filedialog.askopenfilename()
    if file_path == '':
        exit()
    df = pd.read_excel(file_path)
    url = 'http://127.0.0.1:8080/distribuidor/drop-all'
    y = requests.post(url)
    url = 'http://127.0.0.1:8080/distribuidor/crear'
    print(df.shape)
    max = df.shape[0]
    i = 1
    for ind in df.index:
        print(f'Registrando al distribuidor {df["Nombre"][ind]} con el {df["Descuento"][ind]}%. \n{i} de {max}')
        myobj = {
            "nombre": df['Nombre'][ind],
            "descuento": float(df['Descuento'][ind])
        }
        #myobj = json.dumps(myobj)
        x = requests.post(url, json=myobj)

        i += 1
        print(x.text)
    root.destroy()


def ventas_todas():
    url = 'http://127.0.0.1:8080/venta/reporte_ventas_todas'
    from tkinter.filedialog import asksaveasfile
    file_path = asksaveasfile(initialfile='Reporte.xlsx',
                              defaultextension=".xlsx", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])

    if file_path.name == '':
        exit()
    myobj = {
        "path": file_path.name
    }
    x = requests.get(url, json=myobj)
    ventas = x.json()
    print(x.json())
    #for venta in ventas:
    df = pd.DataFrame.from_dict(ventas)
    #print(df)
    df.to_excel(file_path.name)
    for venta in ventas:
        df_info = pd.DataFrame(columns=["codigo", "nombre", "cantidad","precio", "precio_descuento"])
        for producto in venta['productos']:
            new_df = pd.Series({
                "codigo": producto['codigo'],
                "nombre": producto['nombre'],
                "cantidad": producto['cantidad'],
                "precio": producto['precio_lista'],
                "precio_descuento": producto['precio_descuento']
            })
            print(df_info.shape)
            print(new_df.shape)
            df_info.loc[len(df_info)] = new_df

        df_info.to_excel('./reporte_por_pedido'+str(venta['folio'])+'.xlsx')

    exit()



root.title('Sistema de Natural')
title = tk.Label(root, text="Escoge una opción del menú",font=("Arial", 25))
canvas1.create_window(350,50, window=title)

button_inventario = tk.Button(root, text='Cargar inventario', command=cargar_datos, bg='brown', fg='white')
canvas1.create_window(350, 150, window=button_inventario)

button_reporte = tk.Button(root, text='Generar reporte de ventas', command=generar_reporte, bg='brown', fg='white')
canvas1.create_window(350, 250, window=button_reporte)

button_distribuidores = tk.Button(root, text='Subir distribuidores', command=subir_distribuidores, bg='brown',
                                  fg='white')
canvas1.create_window(350, 350, window=button_distribuidores)

button_ventas_todas = tk.Button(root, text='Reporte todas las ventas', command=ventas_todas, bg='brown',
                                  fg='white')
canvas1.create_window(350, 450, window=button_ventas_todas)

root.mainloop()
root = tk.Tk()
root.withdraw()
