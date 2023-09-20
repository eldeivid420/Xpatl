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
        self.roles = None
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
                self.roles = params['roles']
                self.id = post(
                    '''INSERT INTO usuario (username, pass, activo, nombre) values (%s,%s,%s,%s) returning id''',
                    (self.username, self.password, self.estatus, self.nombre), True
                )
                self.id = self.id[0]
                for rol in self.roles:
                    post(
                        '''INSERT INTO usuario_permisos (username, rol) values (%s,%s)''',
                        (self.username, rol)
                    )
            except Exception as e:
                raise Exception(e)

    def load(self, params):

        # verificamos si existe el usuario
        self.username = params['username'].rstrip()
        rol = params['rol']
        exist = get('''SELECT * FROM usuario WHERE username = %s''', (self.username,), False)
        roles = get('''SELECT rol FROM usuario_permisos WHERE username = %s''', (self.username,), True)
        self.roles = []
        [self.roles.append(rol[0]) for rol in roles]
        if exist == None:
            # Checa que el usuario exista
            raise Exception('El usuario no existe')
        h = hashlib.sha256(params['pass'].encode('utf-8')).hexdigest()
        if exist[3] != h:
            # Checa que los hashes de las contraseñas sean iguales
            raise Exception('Contraseña incorrecta')
        if rol not in self.roles:
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
        filtro = params['activos']
        usuarios = []
        registros = get('''SELECT username, nombre FROM usuario WHERE activo = %s''',
                            (filtro,), True)
        if not registros:
            raise Exception('No se encontraron usuarios')

        for i in range(len(registros)):
            roles = get('''SELECT rol FROM usuario_permisos WHERE username = %s''', (registros[i][0],), True)
            roles_list = []
            for rol in roles:
                rolecito = None
                if rol[0] == 'admin':
                    rolecito = 'adm'
                elif rol[0] == 'vendedor':
                    rolecito = 'vts'
                elif rol[0] == 'cobrador':
                    rolecito = 'cob'
                elif rol[0] == 'entregador':
                    rolecito = 'ent'
                roles_list.append(rolecito)
            roles_list = ', '.join(roles_list)
            usuarios.append({'usuario': registros[i][0], 'nombre': registros[i][1], 'area': roles_list})

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
        if params['activo'] == True or params['activo'] == False:
            post('''UPDATE usuario SET  activo = %s WHERE username = %s''', (params['activo'], username), False)
        if params['roles']:
            post('''DELETE FROM usuario_permisos WHERE username = %s''', (username,), False)
            for rol in params['roles']:
                post(
                    '''INSERT INTO usuario_permisos (username, rol) values (%s,%s)''',
                    (username, rol)
                )
            #post('''UPDATE usuario SET rol = %s WHERE username = %s''', (params['rol'], username), False)

        return f'Usuario actualizado existosamente'
