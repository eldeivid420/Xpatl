from Global.Utils.db import post, get
import hashlib
import jwt
import os
# TODO: Documentar


class Usuario:
    def __init__(self, params, load=True):
        self.id = None
        self.username = None
        self.nombre = None
        self.password = None
        self.estatus = None
        self.rol = None
        self.load(params) if load else self.create(params)

    def create(self, params):
        # verificamos si existe el usuario
        self.username = params['username']
        exist = get('''SELECT * FROM usuario WHERE username = %s''', (self.username,), False)
        if exist:
            raise Exception('El usuario ya existe')
        else:
            try:
                h = hashlib.sha256(params['pass'].encode('utf-8')).hexdigest()
                self.password = h
                self.nombre = params['nombre']
                self.estatus = True
                self.rol = params['rol']
                self.id = post(
                    '''INSERT INTO usuario (username, pass, estatus, rol, nombre) values (%s,%s,%s,%s, %s) returning id''',
                    (self.username, self.password, self.estatus, self.rol, self.nombre), True
                )
                self.id = self.id[0]
            except Exception as e:
                raise Exception(e)

    def load(self, params):

        # verificamos si existe el usuario
        self.username = params['username']
        self.rol = params['rol']
        exist = get('''SELECT * FROM usuario WHERE username = %s''', (self.username,), False)
        if exist == None:
            # Checa que el usuario exista
            raise Exception('El usuario no existe')
        h = hashlib.sha256(params['pass'].encode('utf-8')).hexdigest()
        if exist[3] != h:
            # Checa que los hashes de las contraseñas sean iguales
            raise Exception('Contraseña incorrecta')
        if exist[5] != self.rol:
            # Revisa que el rol seleccionado sea igual al que pertenece el usuario
            raise Exception('El usuario no es de este tipo de rol')
        token = os.environ.get('JWT_TOKEN')
        web_token = jwt.encode({
        "username": self.username
        },
            token,
            algorithm='HS256'
        )
        self.web_token = web_token
        return self
        #return str(e), 400
