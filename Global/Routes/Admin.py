from flask import Blueprint
from Global.Controllers import Usuario as u


GLOBAL_ADMIN_BLUEPRINT = Blueprint('GLOBAL_ADMIN_BLUEPRINT', __name__)

@GLOBAL_ADMIN_BLUEPRINT.route('/crear-usuario', methods=['POST'])
def crear_usuario():
    return u.registrar_usuario()

@GLOBAL_ADMIN_BLUEPRINT.route('/obtener-usuarios', methods=['GET'])
def obtener_usuarios():
    return u.obtener_usuarios()


