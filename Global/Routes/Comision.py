from flask import Blueprint
import Global.Controllers.Comision as c

GLOBAL_COMISION_BLUEPRINT = Blueprint('GLOBAL_COMISION_BLUEPRINT', __name__)


@GLOBAL_COMISION_BLUEPRINT.route('/fecha', methods=['GET'])
def buscar_comisiones_fecha():
    return c.buscar_comisiones_fecha()

@GLOBAL_COMISION_BLUEPRINT.route('/todas', methods=['GET'])
def buscar_comisiones():
    return c.buscar_comisiones()