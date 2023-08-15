import json

from flask import request
from Global.Classes.Venta import Venta

# TODO: Documentar


def crear_venta():
    try:
        params = {
            'vendedor': request.json.get('vendedor'),
            'sub_id': request.json.get('sub_id'),
            'tipo': request.json.get('tipo'),
            'estatus': request.json.get('estatus'),
            'proveedor': request.json.get('proveedor'),
            'proveedor_notas': request.json.get('proveedor_notas'),
            'descuento': request.json.get('descuento'),
            'productos': request.json.get('productos')
        }
        venta = Venta(params, False)
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
            "sub_id": venta.sub_id,
            "tipo": venta.tipo,
            "estatus": venta.estatus,
            "proveedor": venta.proveedor,
            "proveedor_notas": venta.proveedor_notas,
            "descuento": venta.descuento,
            "subtotal": venta.subtotal,
            "total": venta.total,
            "productos": venta.productos,
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
