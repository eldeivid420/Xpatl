from flask import request
from Global.Classes.Comision import Comision
import json


def buscar_comisiones_fecha():
    try:
        params = {
            'username': request.json.get('username'),
            'fecha': request.json.get('fecha')
        }
        comisiones = Comision.buscar_comisiones_fecha(params)
        return json.dumps(comisiones)
    except Exception as e:
        return {'error': str(e)}

def pagar_comision():
    pass


def buscar_comisiones():
    try:
        params = {
            'username': request.json.get('username')
        }
        comision = Comision.buscar_comisiones(params)
        return json.dumps(comision)
    except Exception as e:
        return {'error': str(e)}
