from flask import Blueprint
import Global.Controllers.Distribuidor as d

GLOBAL_DISTRIBUIDOR_BLUEPRINT = Blueprint('GLOBAL_DISTRIBUIDOR_BLUEPRINT', __name__)


@GLOBAL_DISTRIBUIDOR_BLUEPRINT.route('/obtener-todos', methods=['GET'])
def obtener_todos():
    return d.obtenerTodos()


