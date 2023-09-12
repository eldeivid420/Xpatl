from flask import request
from Global.Classes.Distribuidor import Distribuidor
import json

def subirDistribuidor():
    try:
        params = {
            "nombre": request.json.get('nombre'),
            "descuento": request.json.get('descuento')
        }
        distribuidor = Distribuidor(params, False)
        return f'Se ha registrado {distribuidor.nombre} con el {distribuidor.descuento}% de descuento.', 200
    except Exception as e:
        return {'error': str(e)}, 400

def obtenerTodos():
    try:
        return Distribuidor.getAll()
    except Exception as e:
        return {'error': str(e)}, 400

def borrarTodos():
    try:
        return Distribuidor.deleteAll()
    except Exception as e:
        return {'error': str(e)}, 400
