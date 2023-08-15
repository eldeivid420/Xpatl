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
        return Venta.load(params)
    except Exception as e:
        return {'error': str(e)}, 400
