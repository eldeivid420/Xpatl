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


@GLOBAL_VENTA_BLUEPRINT.route('/buscar', methods=['GET'])
def buscar_venta():
    return v.buscar_venta()




