"""
    Clase que describe un distribuidor
    Authors: Erick Hernández Silva
    Created: 12/09/2023
    Last update: 14/08/2023
"""

from Global.Utils.db import post, get

class Distribuidor:
    def __init__(self, params, load = True):
        self.id = None
        self.nombre = None
        self.descuento = None
        self.load(params) if load else self.create(params)

    def load(self, params):
        self.id = params['id']
        if self.exist(use_id=True):
            self.id, self.nombre, self.descuento, self.activo = get('''SELECT * FROM distribuidores WHERE id=%s'''
                                                   ,(self.id,),False)
            if not self.activo:
                raise Exception('Este proveedor no está activo')
        else:
            raise Exception('No existe este distribuidor')
    def create(self, params):
        self.nombre = params['nombre']
        self.descuento = params['descuento']
        if self.exist():
            self.id = post(
                '''UPDATE distribuidores SET descuento = %s, activo = %s WHERE nombre = %s returning id''',
                (self.descuento, True, self.nombre), True)
        else:
            self.id = post(
            '''INSERT INTO distribuidores(nombre, descuento) VALUES(%s, %s) returning id''',
            (self.nombre, self.descuento),True)

    def exist(self, use_id = False):
        if use_id:
            exists = get('''SELECT * FROM distribuidores WHERE id = %s''', (self.id,), False)
        else:
          exists = get('''SELECT * FROM distribuidores WHERE nombre = %s''', (self.nombre,), False)
        if exists:
            return True
        else:
            return False

    @classmethod
    def getAll(cls, params):
        activo = params['activo']
        dists = get('''SELECT * FROM distribuidores WHERE activo = %s''', (activo,), True)
        distribuidores = []
        for dist in dists:
            distribuidores.append(
                {
                    'dropdown': dist[1] + ' - {:.2f}%'.format(dist[2]),
                    'id': dist[0],
                    'descuento': dist[2]/100,
                    'nombre': dist[1]
                }
            )
        return distribuidores

    @classmethod
    def deleteAll(cls):
        post('''UPDATE distribuidores set activo=False''', ())
        return 'Borrados'