from Global.Utils.db import post, get


# TODO: Documentar
primera_venta = False


class Venta:

    def __init__(self, params, load=True):
        self.id = None
        self.vendedor = None
        self.sub_id = None
        self.tipo = None
        self.estatus = None
        self.proveedor = None
        self.proveedor_notas = None
        self.descuento = None
        self.subtotal = None
        self.total = None
        self.productos = None
        self.fecha = None
        self.load(params) if load else self.create(params)

    def create(self, params):

        # TODO: implementar funcion que genere sub_id usando el timestamp de la base de datos
        try:
            self.vendedor = params['vendedor']
            self.sub_id = self.obtener_subid()
            self.tipo = params['tipo']
            self.estatus = params['estatus']
            self.proveedor = params['proveedor']
            self.proveedor_notas = params['proveedor_notas']
            self.descuento = params['descuento']
            self.productos = params['productos']

            self.subtotal = self.calcular_subtotal()
            self.total = self.calcular_total()

            # Verificamos si es una venta para un proveedor
            if self.proveedor and self.descuento:

                self.id = post(
                    '''INSERT INTO venta(vendedor,sub_id,tipo,estatus,proveedor,proveedor_notas,descuento,subtotal,total) VALUES(%s,
                    %s,%s,%s,%s,%s,%s,%s,%s) RETURNING id '''
                    , (self.vendedor, self.sub_id, self.tipo, self.estatus, self.proveedor, self.proveedor_notas,
                       self.descuento, self.subtotal, self.total), True)[0]
            # Si no es proveedor, entonces dejamos los campos proveedor y descuento como Null
            else:
                self.id = post(
                    '''INSERT INTO venta(sub_id,tipo,estatus,subtotal,total) VALUES(%s,%s,%s,%s,%s) RETURNING id'''
                    , (self.sub_id, self.tipo, self.estatus, self.subtotal, self.total)
                    , True
                )[0]
            for producto in self.productos:
                post('''INSERT INTO producto_venta(producto, venta) VALUES (%s,%s)''', (producto, self.id), False)
        except Exception as e:
            return str(e), 400

    def exist(self):

        """
        Método que verifica si una venta existe

        Parameters:
        * id: el id de la venta

        Returns:

        True si el la venta existe
        """

        exist = get('''SELECT * FROM venta WHERE id = %s''', (self.id,))
        return exist

    def load(self, params):
        self.id = params['id']
        if self.exist() is None:
            raise Exception('No hay venta con el id proporcionado')
        self.id, self.vendedor, self.sub_id, self.tipo, self.estatus, self.proveedor, self.proveedor_notas, self.descuento, self.subtotal, self.total, self.fecha = get(
            '''SELECT * FROM venta WHERE id = %s''', (self.id,), False)
        self.fecha = self.fecha.strftime("%m/%d/%Y %H:%M:%S")

    @classmethod
    def cancelar_venta(cls, params):
        id = params['id']
        post('''UPDATE venta SET estatus = 'cancelado' WHERE id = %s''', (id,), False)
        return f'Venta cancelada exitosamente'

    def calcular_subtotal(self):

        suma = 0
        for producto in self.productos:
            precio = get('''SELECT precio FROM producto WHERE sku = %s''', (producto,), False)[0]
            suma += precio

        return round(suma, 2)

    def calcular_total(self):
        if self.proveedor:
            total = self.subtotal * self.descuento
            return round(total, 2)
        else:
            return self.subtotal

    def obtener_subid(self):
        if primera_venta:
            self.sub_id = 1
        else:
            id_anterior = get('''SELECT sub_id FROM venta ORDER BY fecha desc limit 1''', (), False)[0]
            self.sub_id = id_anterior+1
        return self.sub_id
