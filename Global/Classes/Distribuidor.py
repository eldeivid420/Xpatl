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
        self.id, self.nombre, self.descuento = get('''SELECT * FROM distribuidores WHERE id=%s'''
                                                   ,(self.id,),False)

    def create(self, params):
        self.nombre = params['nombre']
        self.descuento = params['descuento']
        self.id, self.nombre, self.descuento = post(
            '''INSERT INTO distribuidores(nombre, descuento) VALUES(%s, %s)''',
            (self.nombre, self.descuento),True)


    @classmethod
    def getAll(cls):
        dists = get('''SELECT * FROM distribuidores''', (), False)
        distribuidores = []
        for dist in dists:
            distribuidores.append(
                {
                    'dropdown': dist[1] + ' - ' + dist[2],
                    'id': dist[0],
                    'descuento': dist[2]/100
                }
            )
        return distribuidores