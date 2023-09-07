from flask import request
from Global.Classes.Producto import Producto
import json


def agregar_producto():
    try:
        params = {
            'nombre': request.json.get('nombre'),
            'precio': request.json.get('precio'),
            'precio_esp': request.json.get('precio_esp'),
            'disponibles': request.json.get('disponibles'),
            'sku': request.json.get('sku')
        }
        producto = Producto(params, False)
        return f'Producto registrado con el id: {producto.id}'
    except Exception as e:
        return {'error': str(e)}, 400


def obtener_productos():
    return Producto.obtener_productos()


def eliminar_producto():
    try:
        params = {
            'sku': request.json.get('sku')
        }
        return Producto.eliminar_producto(params)
    except Exception as e:
        return {"error": str(e)}


def buscar_producto():
    try:
        params = {
            'sku': request.json.get('sku')
        }
        producto = Producto(params)
        detalles = {
            "id": producto.id,
            "nombre": producto.nombre,
            "precio": producto.precio,
            "precio_esp": producto.precio_esp,
            "disponibles": producto.disponibles,
            "sku": producto.sku,
            "estatus": producto.estatus
        }
        return json.dumps(detalles)
    except Exception as e:
        return {"error": str(e)}


def editar_producto():
    try:
        params = {
            'nombre': request.json.get('nombre'),
            'precio': request.json.get('precio'),
            'precio_esp': request.json.get('precio_esp'),
            'disponibles': request.json.get('disponibles'),
            'sku': request.json.get('sku'),
            'estatus': request.json.get('estatus')
        }
        producto = Producto(params)
        msg = producto.actualizar_producto(params)
        return msg, 200
    except Exception as e:
        return {"error": str(e)}, 400


def filtrar_productos():
    try:
        params = {
            'orden': request.json.get('orden'),
            'invertido': request.json.get('invertido')
        }
        return Producto.filtrar_productos(params)
    except Exception as e:
        return {"error": str(e)}

def drop_all():
    try:
        Producto.drop_all()
        return 'Done'
    except Exception as e:
        return {"error": str(e)}

def cargar_productos():
    try:
        params = {
            'nombre': request.json.get('nombre'),
            'precio': request.json.get('precio'),
            'precio_esp': request.json.get('precio_esp'),
            'disponibles': request.json.get('disponibles'),
            'sku': request.json.get('sku'),
            'override': True
        }
        producto = Producto(params, False)
        return f'Producto registrado con el id: {producto.id}'
    except Exception as e:
        return {'error': str(e)}, 400