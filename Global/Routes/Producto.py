from flask import Blueprint
from Global.Controllers import Producto as p

# TODO: Documentar


GLOBAL_PRODUCTO_BLUEPRINT = Blueprint('GLOBAL_PRODUCTO_BLUEPRINT', __name__)


@GLOBAL_PRODUCTO_BLUEPRINT.route('/agregar', methods=['POST'])
def agregar_producto():
    return p.agregar_producto()


@GLOBAL_PRODUCTO_BLUEPRINT.route('/todos', methods=['GET'])
def obtener_productos():
    return p.obtener_productos()