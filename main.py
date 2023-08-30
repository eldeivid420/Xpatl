from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from Global.Utils.db import get
import datetime
import Global.Classes.Venta as v
# Backend config
load_dotenv()
application = Flask(__name__)
cors = CORS(application)


# Ruta de testing
@application.route("/")
def hello_there():
    return "General Kenobi", 200

# Registro de blueprints


from Global.Routes.Venta import GLOBAL_VENTA_BLUEPRINT
from Global.Routes.Producto import GLOBAL_PRODUCTO_BLUEPRINT
from Global.Routes.Usuario import GLOBAL_USUARIO_BLUEPRINT
from Global.Routes.Comision import GLOBAL_COMISION_BLUEPRINT
from Global.Routes.Admin import GLOBAL_ADMIN_BLUEPRINT

application.register_blueprint(GLOBAL_VENTA_BLUEPRINT, url_prefix='/venta')
application.register_blueprint(GLOBAL_PRODUCTO_BLUEPRINT, url_prefix='/producto')
application.register_blueprint(GLOBAL_USUARIO_BLUEPRINT, url_prefix ='/usuario')
application.register_blueprint(GLOBAL_COMISION_BLUEPRINT, url_prefix ='/comision')
application.register_blueprint(GLOBAL_ADMIN_BLUEPRINT, url_prefix ='/admin')
print('La aplicación está funcionando... \n\nNO cierre esta ventana.')

try:
    dia_anterior = get('''SELECT fecha FROM venta ORDER BY fecha DESC LIMIT 1''', (), False)[0]
    dia_hoy = datetime.datetime.now()
    #dia_hoy = f'{dia_hoy.day}/{dia_hoy.month}/{dia_hoy.year}'
    dia_hoy = dia_hoy.strftime("%d/%m/%Y")
    dia_anterior = dia_anterior.strftime("%d/%m/%Y")
    if dia_hoy == dia_anterior:
        d_anterior = get('''SELECT sub_id FROM venta ORDER BY fecha desc limit 1''', (), False)[0]
        v.primera_venta = d_anterior + 1
    else:
        v.primera_venta = 1
except:
    v.primera_venta = 1


if __name__ == "__main__":
    application.run(host="0.0.0.0", debug=True, port=os.environ.get('FLASK_PORT'))
# print(message.sid)

