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
        return comisiones, 200
    except Exception as e:
        return {'error': str(e)}, 400

def pagar_comision():
    try:
        params = {'id': request.json.get('id')}
        return Comision.pagar_comision(params), 200
    except Exception as e:
        return {'error': str(e)}, 400


def buscar_comisiones():
    try:
        params = {
            'username': request.json.get('username')
        }
        comision = Comision.buscar_comisiones(params)
        return json.dumps(comision)
    except Exception as e:
        return {'error': str(e)}


def registros_dia():
    try:
        params = {
            'fecha': request.json.get('fecha')
        }
        return Comision.registros_dia(params)
    except Exception as e:
        return {'error': str(e)}, 400

def comision_usuario_hoy():
    try:
        params = {'username': request.json.get('username')}
        return Comision.comision_usuario_hoy(params), 200
    except Exception as e:
        return {'error': str(e)}, 400
