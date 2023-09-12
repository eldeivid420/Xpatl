import json
import win32print
import win32api
import os

from flask import request
from Global.Classes.Venta import Venta

# TODO: Documentar


def print_pdf(params):
    """ # A List containing the system printers
    all_printers = [printer[2] for printer in win32print.EnumPrinters(2)]
    # Ask the user to select a printer
    printer_num = int(input("Choose a printer:\n" + "\n".join([f"{n} {p}" for n, p in enumerate(all_printers)]) + "\n"))
    # set the default printer
    win32print.SetDefaultPrinter(all_printers[printer_num])
    pdf_dir = "D:/path/to/pdf_dir/**/*"
    for f in glob(pdf_dir, recursive=True):
        win32api.ShellExecute(0, "print", f, None, ".", 0)"""

    all_printers = [printer[2] for printer in win32print.EnumPrinters(2)]
    win32print.SetDefaultPrinter(all_printers[0])
    pdf_dir = "./recibos/" + str(params['id']) + ".pdf"
    pdf_dir = os.path.abspath(pdf_dir)
    pdf_dir = pdf_dir.replace('\\', '/')
    os.listdir('./recibos')
    win32api.ShellExecute(0, "print", pdf_dir, None, ".", 0)


def crear_venta():
    try:
        params = {
            'vendedor': request.json.get('vendedor'),
            'comprador': request.json.get('comprador'),
            'proveedor': request.json.get('proveedor'),
            'proveedor_notas': request.json.get('proveedor_notas'),
            'descuento': request.json.get('descuento'),
            'productos': request.json.get('productos')
        }
        venta = Venta(params, False)
        return f'Venta registrada con el id {venta.sub_id}', 200
    except Exception as e:
        if str(e) != 'Ocurrió un error inesperado, por favor vuelva a crear el pedido':
            diccionario = json.loads(str(e))
            return {'error': diccionario}, 400
        else:
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
            "metodos_pago": venta.metodos,
            "estatus": venta.estatus,
            "comprador": venta.comprador,
            "proveedor": venta.proveedor,
            "proveedor_notas": venta.proveedor_notas,
            "descuento": venta.descuento,
            "subtotal": venta.subtotal,
            "total": venta.total,
            "productos": venta.detalles_productos,
            "fecha": venta.fecha,
            "factura": venta.factura
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
            'metodos': request.json.get('metodos')
        }
        Venta.pagar_venta(params)
        venta = Venta(params)
        venta.generar_pdf()
        print_pdf(params)
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
        return Venta.fechas_venta()
    except Exception as e:
        return {'error': str(e)}, 400


def registros_dia():
    try:
        params = {
            'fecha': request.json.get('fecha')
        }
        return Venta.registgros_dia(params)
    except Exception as e:
        return {'error': str(e)}, 400


def cobrador_pedidos():
    try:
        return Venta.cobrador_pedidos()
    except Exception as e:
        return {'error': str(e)}, 400

def entregador_pedidos():
    try:
        return Venta.entregador_pedidos()
    except Exception as e:
        return {'error': str(e)}, 400


def fechas_evento():
    """
    Parameters:
    * reciente: true -> de más reciente a menos reciente; false -> de menos reciente a más reciente
    * pagos: 'normal' -> todos los pagos; 'pendiente' -> sólo los pagos pendientes; 'pagado' -> sólo pagos completados
    Returns:

    Una lista de diccionarios con la información

    """
    try:
        params = {'reciente': request.json.get('reciente'),
                  'pagos': request.json.get('pagos')}
        return Venta.fechas_evento(params)
    except Exception as e:
        return {'error': str(e)}, 400


def detalles_pedido():
    try:
        params = {'id': request.json.get('id')}
        return Venta.detalles_pedido(params)
    except Exception as e:
        return {'error': str(e)}, 400

def reporte():
    try:
        params = {
            "path": request.json.get('path')
        }
        return Venta.reporte(params)
    except Exception as e:
        return {'error': str(e)}, 400


def comisiones_dia():
    try:
        params = {
            'fecha': request.json.get('fecha')
        }
        return Venta.comisiones_dia(params)
    except Exception as e:
        return {'error': str(e)}, 400

def metodos_pago():
    try:
        return Venta.getMethods(), 200
    except Exception as e:
        return {'error': str(e)}, 400