import json

from flask import request
from Global.Classes.Venta import Venta

# TODO: Documentar


def crear_venta():
    try:
        params = {
            'vendedor': request.json.get('vendedor'),
            'proveedor': request.json.get('proveedor'),
            'proveedor_notas': request.json.get('proveedor_notas'),
            'descuento': request.json.get('descuento'),
            'productos': request.json.get('productos')
        }
        try:
            venta = Venta(params, False)
        except Exception as e:
            return {'error': str(e)}, 400
        return f'Venta registrada con el id {venta.id}', 200
    except Exception as e:
        return {'error': str(e)}, 400


def buscar_venta():
    try:
        params = {
            'id': request.json.get('id')
        }
        venta = Venta(params)
        detalles = {
            "id": venta.id,
            "vendedor": venta.vendedor,
            "tipo": venta.tipo,
            "estatus": venta.estatus,
            "proveedor": venta.proveedor,
            "proveedor_notas": venta.proveedor_notas,
            "descuento": venta.descuento,
            "subtotal": venta.subtotal,
            "total": venta.total,
            "productos": venta.detalles_productos,
            "fecha": venta.fecha
        }
        return json.dumps(detalles)
    except Exception as e:
        return {'error': str(e)}, 400


def cancelar_venta():
    try:
        params ={
            'id': request.json.get('id')
        }
        return Venta.cancelar_venta(params)
    except Exception as e:
        return {'error': str(e)}, 400


def pagar_venta():
    try:
        params = {
            'id': request.json.get('id'),
            'tipo': request.json.get('tipo')
        }
        Venta.pagar_venta(params)
        return f'Pago realizado exitosamente'
    except Exception as e:
        return {'error': str(e)}, 400


def entregar_venta():
    try:
        params = {
            'id': request.json.get('id')
        }
        Venta.entregar_venta(params)
        venta = Venta(params)
        info = []
        for i in range(len(venta.detalles_productos)):
            info.append({'nombre': venta.detalles_productos[i]["nombre"], "cantidad": venta.detalles_productos[i]["cantidad"]})
        detalles = {
            "productos": info
        }
        return json.dumps(detalles)
    except Exception as e:
        return {'error': str(e)}, 400

'''def registros_dia():
    try:
        params = {
            'fecha': request.json.get('fecha')
        }
        registros = []
        registros.append(Venta.registros_dia())
    except Exception as e:
        return {'error': str(e)}, 400'''


def fechas_venta():
    try:
        return json.dumps(Venta.fechas_venta())
    except Exception as e:
        return {'error': str(e)}, 400