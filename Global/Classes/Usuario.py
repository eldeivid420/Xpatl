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
                    '''INSERT INTO usuario (username, pass, activo, rol, nombre) values (%s,%s,%s,%s, %s) returning id''',
                    (self.username, self.password, self.estatus, self.rol, self.nombre), True
                )
                self.id = self.id[0]
            except Exception as e:
                raise Exception(e)

    def load(self, params):

        # verificamos si existe el usuario
        self.username = params['username'].rstrip()
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
            raise Exception('El usuario no pertenece a esta área')
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

    @classmethod
    def obtener_usuarios(cls, params):
        filtro = params['filtro']
        usuarios = []

        if filtro == 'admin':
            registros = get('''SELECT username, nombre, rol FROM usuario WHERE rol = 'admin'  and activo = true''',
                            (filtro,), True)
        elif filtro == 'vendedor':
            registros = get('''SELECT username, nombre, rol FROM usuario WHERE rol = 'vendedor'  and activo = true''',
                            (filtro,), True)
        elif filtro == 'cobrador':
            registros = get('''SELECT username, nombre, rol FROM usuario WHERE rol = 'cobrador'  and activo = true''',
                            (filtro,), True)
        elif filtro == 'entregador':
            registros = get('''SELECT username, nombre, rol FROM usuario WHERE rol = 'entregador'  and activo = true''',
                            (filtro,), True)
        elif not filtro:
            registros = get('''SELECT username, nombre, rol FROM usuario WHERE activo = true''',
                            (filtro,), True)
        else:
            raise Exception('Selecciona un filtro válido')

        if not registros:
            raise Exception('No se encontraron usuarios')

        for i in range(len(registros)):
            usuarios.append({'usuario': registros[i][0], 'nombre': registros[i][1], 'area': registros[i][2]})

        return usuarios

    @classmethod
    def editar_usuario(cls, params):
        username = params['username']
        exist = get('''SELECT id FROM usuario WHERE username = %s''', (username,), False)
        if not exist:
            raise Exception("El nombre de usuario no está registrado")
        if params['nombre']:
            post('''UPDATE usuario SET nombre = %s WHERE username = %s''', (params['nombre'], username), False)
        if params['pass']:
            h = hashlib.sha256(params['pass'].encode('utf-8')).hexdigest()
            post('''UPDATE usuario SET pass = %s WHERE username = %s''', (h, username), False)
        if params['activo']:
            post('''UPDATE usuario SET  activo = %s WHERE username = %s''', (params['activo'], username), False)
        if params['rol']:
            post('''UPDATE usuario SET rol = %s WHERE username = %s''', (params['rol'], username), False)

        return f'Usuario actualizado existosamente'
