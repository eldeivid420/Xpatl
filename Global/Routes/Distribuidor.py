from flask import Blueprint
import Global.Controllers.Distribuidor as d

GLOBAL_DISTRIBUIDOR_BLUEPRINT = Blueprint('GLOBAL_DISTRIBUIDOR_BLUEPRINT', __name__)


@GLOBAL_DISTRIBUIDOR_BLUEPRINT.route('/obtener-todos', methods=['GET'])
def obtener_todos():
    return d.obtenerTodos()


@GLOBAL_DISTRIBUIDOR_BLUEPRINT.route('/crear', methods=['POST'])
def crear():
    return d.subirDistribuidor()

@GLOBAL_DISTRIBUIDOR_BLUEPRINT.route('/drop-all', methods=['POST'])
def borrar():
    return d.borrarTodos()