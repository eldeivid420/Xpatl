from flask import Blueprint
from Global.Controllers import Venta as v

# TODO: Documentar


GLOBAL_VENTA_BLUEPRINT = Blueprint('GLOBAL_VENTA_BLUEPRINT', __name__)


@GLOBAL_VENTA_BLUEPRINT.route('/crear', methods=['POST'])
def crear_venta():
    return v.crear_venta()


@GLOBAL_VENTA_BLUEPRINT.route('/cancelar', methods=['POST'])
def cancelar_venta():
    return v.cancelar_venta()


@GLOBAL_VENTA_BLUEPRINT.route('/pagar', methods=['POST'])
def pagar_venta():
    return v.pagar_venta()

@GLOBAL_VENTA_BLUEPRINT.route('/entregar', methods=['POST'])
def entregar_venta():
    return v.entregar_venta()


@GLOBAL_VENTA_BLUEPRINT.route('/admin/buscar', methods=['POST'])
def buscar_venta():
    return v.buscar_venta()

#TODO se está usando?
@GLOBAL_VENTA_BLUEPRINT.route('/admin/fechas-venta', methods=['GET'])
def fechas_venta():
    return v.fechas_venta()

@GLOBAL_VENTA_BLUEPRINT.route('/admin/dia', methods=['POST'])
def registros_dia():
    return v.registros_dia()

@GLOBAL_VENTA_BLUEPRINT.route('/cobrador-pedidos', methods=['GET'])
def cobrador_pedidos():
    return v.cobrador_pedidos()


@GLOBAL_VENTA_BLUEPRINT.route('/entregador-pedidos', methods=['GET'])
def entregador_pedidos():
    return v.entregador_pedidos()

@GLOBAL_VENTA_BLUEPRINT.route('/admin/fechas-evento', methods=['POST'])
def fechas_evento():
    return v.fechas_evento()

@GLOBAL_VENTA_BLUEPRINT.route('/admin/detalles-pedido', methods=['POST'])
def detalles_pedido():
    return v.detalles_pedido()

@GLOBAL_VENTA_BLUEPRINT.route('/admin/comisiones-dia', methods=['POST'])
def comisiones_dia():
    return v.comisiones_dia()


@GLOBAL_VENTA_BLUEPRINT.route('/admin/facturas/pendientes', methods=['GET'])
def facturas_pendientes():
    return v.facturas_pendientes()


@GLOBAL_VENTA_BLUEPRINT.route('/admin/facturas/facturar', methods=['POST'])
def facturas_facturar():
    return v.facturas_facturar()


@GLOBAL_VENTA_BLUEPRINT.route('/admin/editar-proveedor', methods=['POST'])
def editar_proveedor():
    return v.editar_proveedor()

@GLOBAL_VENTA_BLUEPRINT.route('/reporte', methods=['POST'])
def reporte():
    return v.reporte()

@GLOBAL_VENTA_BLUEPRINT.route('/metodos-pago', methods=['GET'])
def metodos_pago():
    return v.metodos_pago()

@GLOBAL_VENTA_BLUEPRINT.route('/reporte_ventas_todas', methods=['GET'])
def ventas_todas():
    return v.ventas_todas()
