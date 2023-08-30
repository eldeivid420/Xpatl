from flask import Blueprint
from Global.Controllers import Usuario as u


GLOBAL_USUARIO_BLUEPRINT = Blueprint('GLOBAL_USUARIO_BLUEPRINT', __name__)


@GLOBAL_USUARIO_BLUEPRINT.route('/login', methods=['POST'])
def iniciar_sesion():
    return u.iniciar_sesion()



