from Global.Utils.db import post, get


class Venta:

    def __init__(self, params, load=True):
        self.id = None
        self.sub_id = None
        self.tipo = None
        self.estatus = None
        self.proveedor = None
        self.descuento = None
        self.subtotal = None
        self.total = None
        self.productos = None
        self.load(params) if load else self.create(params)

    def create(self, params):
        # TODO: implementar funcion que genere sub_id usando el timestamp de la base de datos
        try:
            self.productos = list(params['productos'])
            self.sub_id = params['sub_id']
            self.tipo = params['tipo']
            self.estatus = params['estatus']
            self.proveedor = params['proveedor']
            self.descuento = params['descuento']
            self.subtotal = self.calcular_subtotal()
            self.total = self.calcular_total()

            # Verificamos si es una venta para un proveedor
            if self.proveedor and self.descuento:

                self.id = post(
                    '''INSERT INTO venta(sub_id,tipo,estatus,proveedor,descuento,subtotal,total) VALUES(%s,%s,%s,%s,%s,
                    %s,%s) RETURNING id'''
                    , (self.sub_id, self.tipo, self.estatus, self.proveedor, self.descuento, self.subtotal, self.total)
                    , True
                )[0]
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

    def load(self, params):
        self.id = params['id']
        try:
            self.sub_id, self.tipo, self.estatus, self.proveedor, self.descuento, self.subtotal, self.total = get(
                '''SELECT * FROM venta WHERE id = %s''', (self.id,), False)
        except Exception as e:
            return str(e), 400

    def calcular_subtotal(self):
        suma = 0
        for producto in self.productos:
            precio = get('''SELECT precio FROM producto WHERE sku = %s''', (producto,), False)[0]
            suma += precio

        return suma

    def calcular_total(self):
        if self.proveedor:
            total = self.subtotal * self.descuento
            return total
        else:
            return self.subtotal

    def obtener_subid(self):
        pass
