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


'''# Blueprints 
from Global.Routes.Incoming import GLOBAL_STORE_BLUEPRINT
application.register_blueprint(GLOBAL_STORE_BLUEPRINT, url_prefix='/incoming')'''

if __name__ == "__main__":
    application.run(host="0.0.0.0", debug=True, port=os.environ.get('FLASK_PORT'))
# print(message.sid)
