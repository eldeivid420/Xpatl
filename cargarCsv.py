import requests
import pandas as pd
df = pd.read_csv('productos.csv')
url = 'http://127.0.0.1:8080/producto/agregar'
print(df.shape)
max = df.shape[0]
i = 1
for ind in df.index:
    print(f'Cargando producto {df["Clave"][ind]}. \n{i} de {max}')
    myobj = {
            'nombre': df['Descripción'][ind],
            'precio': 0,
            'precio_esp': 0,
            'disponibles': df['Existencia'][ind],
            'sku': df['Clave'][ind]
    }
    x = requests.post(url, json = myobj)
    i += 1
    print(x.text)