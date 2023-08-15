from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

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

application.register_blueprint(GLOBAL_VENTA_BLUEPRINT, url_prefix='/venta')
application.register_blueprint(GLOBAL_PRODUCTO_BLUEPRINT, url_prefix='/producto')
application.register_blueprint(GLOBAL_USUARIO_BLUEPRINT, url_prefix ='/usuario')
print('La aplicación está funcionando... \n\nNO cierre esta ventana.')
if __name__ == "__main__":
    application.run(host="0.0.0.0", debug=True, port=os.environ.get('FLASK_PORT'))
# print(message.sid)

