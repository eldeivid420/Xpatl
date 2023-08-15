from flask import Blueprint
from Global.Controllers import Producto as p

# TODO: Documentar


GLOBAL_PRODUCTO_BLUEPRINT = Blueprint('GLOBAL_PRODUCTO_BLUEPRINT', __name__)


@GLOBAL_PRODUCTO_BLUEPRINT.route('/agregar', methods=['POST'])
def agregar_producto():
    return p.agregar_producto()


@GLOBAL_PRODUCTO_BLUEPRINT.route('/eliminar', methods=['POST'])
def eliminar_producto():
    return p.eliminar_producto()


@GLOBAL_PRODUCTO_BLUEPRINT.route('/editar', methods=['POST'])
def editar_producto():
    return p.editar_producto()


@GLOBAL_PRODUCTO_BLUEPRINT.route('/buscar', methods=['GET'])
def buscar_producto():
    return p.buscar_producto()


@GLOBAL_PRODUCTO_BLUEPRINT.route('/todos', methods=['GET'])
def obtener_productos():
    return p.obtener_productos()


@GLOBAL_PRODUCTO_BLUEPRINT.route('/filtrar', methods=['GET'])
def filtrar_productos():
    return p.filtrar_productos()
