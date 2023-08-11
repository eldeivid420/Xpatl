from flask import Blueprint
from Global.Controllers import Venta as v

# TODO: Documentar


GLOBAL_VENTA_BLUEPRINT = Blueprint('GLOBAL_VENTA_BLUEPRINT', __name__)


@GLOBAL_VENTA_BLUEPRINT.route('/crear', methods=['POST'])
def crear_venta():
    return v.crear_venta()


