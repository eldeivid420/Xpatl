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


@GLOBAL_VENTA_BLUEPRINT.route('/buscar', methods=['GET'])
def buscar_venta():
    return v.buscar_venta()

@GLOBAL_VENTA_BLUEPRINT.route('/fechas-venta', methods=['GET'])
def fechas_venta():
    return v.fechas_venta()

@GLOBAL_VENTA_BLUEPRINT.route('/dia', methods=['GET'])
def registros_dia():
    return v.registros_dia()

@GLOBAL_VENTA_BLUEPRINT.route('/cobrador-pedidos', methods=['GET'])
def cobrador_pedidos():
    return v.cobrador_pedidos()


@GLOBAL_VENTA_BLUEPRINT.route('/entregador-pedidos', methods=['GET'])
def entregador_pedidos():
    return v.entregador_pedidos()

@GLOBAL_VENTA_BLUEPRINT.route('/fechas-evento', methods=['GET'])
def fechas_evento():
    return v.fechas_evento()



