from Global.Utils.db import post, get
import hashlib

# TODO: Documentar


class Usuario:
    def __init__(self, params, load=True):
        self.id = None
        self.username = None
        self.password = None
        self.estatus = None
        self.rol = None
        self.load(params) if load else self.create(params)

    def create(self, params):

        # verificamos si existe el usuario
        self.username = params['username']
        exist = get('''SELECT * FROM usuario WHERE username = %s''', (self.username,))

        if exist:
            return 'El usuario ya existe', 400
        else:
            try:
                h = hashlib.sha256(params['pass'].encode('utf-8')).hexdigest()
                self.password = h
                self.estatus = params['estatus']
                self.rol = params['rol']
                self.id = post(
                    '''INSERT INTO usuario (username, pass, estatus, rol) values (%s,%s,%s,%s)''',
                    (self.username, self.password, self.estatus, self.rol), True
                )
            except Exception as e:
                return str(e), 400

    def load(self, params):

        # verificamos si existe el usuario
        self.username = params['username']
        exist = get('''SELECT * FROM usuario WHERE username = %s''', (self.username,))

        if exist:
            try:
                h = hashlib.sha256(params['pass'].encode('utf-8')).hexdigest()
                self.estatus, self.rol = get(
                    '''SELECT * FROM usuario WHERE pass = %s''', (h,), False)
            except Exception as e:
                return str(e), 400
        else:
            return 'El usuario no existe', 400
