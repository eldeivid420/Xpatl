import json

from Global.Utils.db import post, get
import datetime
from fpdf import FPDF, FlexTemplate
from Global.Classes.Distribuidor import Distribuidor

# TODO: Documentar
primera_venta = 1

template = [
    {'name': 'border', 'type': 'B', 'x1': 10.0, 'y1': 10., 'x2': 205.9, 'y2': 269.4},
    {'name': 'company_logo', 'type': 'I', 'x1': 20.0, 'y1': 20.0, 'x2': 65.0, 'y2': 40.0, 'font': None,
     'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 'align': 'L', 'text': 'logo', 'priority': 2,
     'multiline': False},
    {'name': 'fecha', 'type': 'T', 'x1': 160.0, 'y1': 25.0, 'x2': 190.0, 'y2': 37.5, 'font': 'helvetica',
     'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'align': 'C', 'text': '', 'priority': 2,
     'multiline': False},
    {'name': 'subid', 'type': 'T', 'x1': 160.0, 'y1': 35.0, 'x2': 183.0, 'y2': 37.5, 'font': 'helvetica',
     'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'align': 'C', 'text': 'Pedido', 'priority': 2,
     'multiline': False},
    {'name': 'subid_valor', 'type': 'T', 'x1': 175.0, 'y1': 35.0, 'x2': 190.0, 'y2': 37.5, 'font': 'helvetica',
     'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'align': 'C', 'text': '', 'priority': 2,
     'multiline': False},
    {'name': 'title', 'type': 'T', 'x1': 70.0, 'y1': 55.0, 'x2': 140.0, 'y2': 37.5, 'font': 'helvetica',
     'size': 12.0, 'bold': 1, 'italic': 0, 'underline': 0, 'align': 'C', 'text': '', 'priority': 2,
     'multiline': False},
    {'name': 'productos', 'type': 'T', 'x1': 20.0, 'y1': 60.0, 'x2': 50.0, 'y2': 65.0, 'font': 'helvetica',
     'size': 12, 'bold': 1, 'italic': 0, 'underline': 0, 'align': 'L', 'text': 'PRODUCTOS', 'priority': 2,
     'multiline': False},
    {'name': 'precios', 'type': 'T', 'x1': 85.0, 'y1': 60.0, 'x2': 130.0, 'y2': 65.0, 'font': 'helvetica',
     'size': 12, 'bold': 1, 'italic': 0, 'underline': 0, 'align': 'L', 'text': 'PRECIO X UNIDAD',
     'priority': 2, 'multiline': False},
    {'name': 'cantidades', 'type': 'T', 'x1': 135.0, 'y1': 60.0, 'x2': 165.0, 'y2': 65.0,
     'font': 'helvetica', 'size': 12, 'bold': 1, 'italic': 0, 'underline': 0, 'align': 'L',
     'text': 'CANTIDAD', 'priority': 2, 'multiline': False},
    {'name': 'totales', 'type': 'T', 'x1': 175.0, 'y1': 60.0, 'x2': 195.0, 'y2': 65.0, 'font': 'helvetica',
     'size': 12, 'bold': 1, 'italic': 0, 'underline': 0, 'align': 'L', 'text': 'TOTAL', 'priority': 2,
     'multiline': False}

]

subtemplate = [{'name': 'distribuidor', 'type': 'T', 'x1': 20.0, 'y1': 240.0, 'x2': 195.0, 'y2': 215.0,
                'font': 'helvetica', 'size': 12, 'bold': 1, 'italic': 0, 'underline': 0, 'align': 'L',
                'text': '', 'priority': 2, 'multiline': False},
               {'name': 'distribuidor_nombre', 'type': 'T', 'x1': 85.0, 'y1': 230.0, 'x2': 180.0, 'y2': 225.0,
                'font': 'helvetica', 'size': 12, 'bold': 0, 'italic': 0, 'underline': 0, 'align': 'L', 'text': '',
                'priority': 2, 'multiline': True},
               {'name': 'distribuidor_nombre2', 'type': 'T', 'x1': 71.0, 'y1': 230.0, 'x2': 180.0, 'y2': 225.0,
                'font': 'helvetica', 'size': 12, 'bold': 0, 'italic': 0, 'underline': 0, 'align': 'L', 'text': '',
                'priority': 2, 'multiline': True},

               {'name': 'subtotal', 'type': 'T', 'x1': 20.0, 'y1': 240.0, 'x2': 65.0, 'y2': 240.0, 'font': 'helvetica',
                'size': 12, 'bold': 1, 'italic': 0, 'underline': 0, 'align': 'L', 'text': '', 'priority': 2,
                'multiline': False},
               {'name': 'monto_subtotal', 'type': 'T', 'x1': 65.0, 'y1': 240.0, 'x2': 105.0, 'y2': 240.0,
                'font': 'helvetica', 'size': 12, 'bold': 0, 'italic': 0, 'underline': 0, 'align': 'L',
                'text': '', 'priority': 2, 'multiline': False},

               {'name': 'subtotal2', 'type': 'T', 'x1': 20.0, 'y1': 240.0, 'x2': 65.0, 'y2': 240.0, 'font': 'helvetica',
                'size': 12, 'bold': 1, 'italic': 0, 'underline': 0, 'align': 'L', 'text': '', 'priority': 2,
                'multiline': False},
               {'name': 'monto_subtotal2', 'type': 'T', 'x1': 65.0, 'y1': 240.0, 'x2': 105.0, 'y2': 240.0,
                'font': 'helvetica', 'size': 12, 'bold': 0, 'italic': 0, 'underline': 0, 'align': 'L',
                'text': '', 'priority': 2, 'multiline': False},

               {'name': 'descuento', 'type': 'T', 'x1': 20.0, 'y1': 245.0, 'x2': 65.0, 'y2': 245.0,
                'font': 'helvetica', 'size': 12, 'bold': 1, 'italic': 0, 'underline': 0, 'align': 'L',
                'text': 'DESCUENTO:', 'priority': 2, 'multiline': False},
               {'name': 'monto_descuento', 'type': 'T', 'x1': 65.0, 'y1': 245.0, 'x2': 105.0, 'y2': 245.0,
                'font': 'helvetica', 'size': 12, 'bold': 0, 'italic': 0, 'underline': 0, 'align': 'L',
                'text': '', 'priority': 2, 'multiline': False},

               {'name': 'total', 'type': 'T', 'x1': 20.0, 'y1': 255.0, 'x2': 65.0, 'y2': 255.0, 'font': 'helvetica',
                'size': 12, 'bold': 1, 'italic': 0, 'underline': 0, 'align': 'L', 'text': 'TOTAL:', 'priority': 2,
                'multiline': False},
               {'name': 'monto_total', 'type': 'T', 'x1': 65.0, 'y1': 255.0, 'x2': 105.0, 'y2': 255.0,
                'font': 'helvetica', 'size': 12, 'bold': 0, 'italic': 0, 'underline': 0, 'align': 'L',
                'text': '', 'priority': 2, 'multiline': False},

               {'name': 'id', 'type': 'T', 'x1': 100.0, 'y1': 240.0, 'x2': 130.0, 'y2': 240.0,
                'font': 'helvetica', 'size': 12, 'bold': 1, 'italic': 0, 'underline': 0, 'align': 'L',
                'text': 'FOLIO:', 'priority': 2, 'multiline': False},
               {'name': 'id_valor', 'type': 'T', 'x1': 115.0, 'y1': 240.0, 'x2': 150.0, 'y2': 240.0,
                'font': 'helvetica', 'size': 12, 'bold': 0, 'italic': 0, 'underline': 0, 'align': 'L',
                'text': '', 'priority': 2, 'multiline': False},

               {'name': 'metodo', 'type': 'T', 'x1': 100.0, 'y1': 245.0, 'x2': 150.0, 'y2': 245.0, 'font': 'helvetica',
                'size': 12, 'bold': 1, 'italic': 0, 'underline': 0, 'align': 'L', 'text': 'MÉTODO DE PAGO:',
                'priority': 2, 'multiline': False},

               {'name': 'metodo_texto', 'type': 'T', 'x1': 100.0, 'y1': 250.0, 'x2': 150.0, 'y2': 250.0,
                'font': 'helvetica', 'size': 8, 'bold': 0, 'italic': 0, 'underline': 0, 'align': 'L',
                'text': '', 'priority': 2, 'multiline': False},
               {'name': 'metodo_texto2', 'type': 'T', 'x1': 150.0, 'y1': 250.0, 'x2': 200.0, 'y2': 250.0,
                'font': 'helvetica', 'size': 8, 'bold': 0, 'italic': 0, 'underline': 0, 'align': 'L',
                'text': '', 'priority': 2, 'multiline': False},
               {'name': 'metodo_texto3', 'type': 'T', 'x1': 100.0, 'y1': 255.0, 'x2': 150.0, 'y2': 255.0,
                'font': 'helvetica', 'size': 8, 'bold': 0, 'italic': 0, 'underline': 0, 'align': 'L',
                'text': '', 'priority': 2, 'multiline': False},
               {'name': 'metodo_texto4', 'type': 'T', 'x1': 150.0, 'y1': 255.0, 'x2': 200.0, 'y2': 255.0,
                'font': 'helvetica', 'size': 8, 'bold': 0, 'italic': 0, 'underline': 0, 'align': 'L',
                'text': '', 'priority': 2, 'multiline': False}]


class Venta:

    def __init__(self, params, load=True):
        self.id = None
        self.vendedor = None
        self.sub_id = None
        self.factura = None
        self.estatus = None
        self.comprador = None
        self.proveedor = None
        self.proveedor_notas = None
        self.descuento = None
        self.subtotal = None
        self.total = None
        self.comision = None
        self.productos = None
        self.detalles_productos = []
        self.fecha = None
        self.metodos = None
        self.load(params) if load else self.create(params)

    def create(self, params):

        # TODO: implementar funcion que genere sub_id usando el timestamp de la base de datos

        self.vendedor = params['vendedor']
        self.sub_id = self.obtener_subid()
        self.comprador = params['comprador']
        self.proveedor = params['proveedor']
        self.proveedor_notas = params['proveedor_notas']
        self.descuento = None
        self.productos = params['productos']
        self.subtotal = self.calcular_subtotal()
        self.total = self.calcular_total()
        self.comision = (self.subtotal * 0.8) * 0.1
        self.factura = params['factura']
        if len(self.productos) == 0:
            raise Exception('No puedes generar una venta vacía')

        productos_agotados = []
        productos_insuficientes = []
        for producto in self.productos:
            disponible, nombre, sku = get('''SELECT disponibles, nombre, sku FROM producto WHERE sku = %s''',
                                          (producto['sku'],),
                                          False)
            # print(f'NOMBRE {nombre}  DISP: {disponible}')
            if disponible == 0:
                productos_agotados.append(sku)
            elif disponible < producto['cantidad']:
                productos_insuficientes.append({'sku': sku, 'disponibles': disponible})

        if len(productos_agotados) != 0 or len(productos_insuficientes) != 0:
            info = {'productos_insuficientes': productos_insuficientes, 'productos_agotados': productos_agotados}
            raise Exception(json.dumps(info))

        # Verificamos si es una venta para un proveedor
        if self.proveedor:
            self.comision = 0
            self.id = post(
                '''INSERT INTO venta(vendedor,sub_id,comprador,proveedor,proveedor_notas,descuento,subtotal,total,comision,factura) 
                VALUES(%s, %s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id'''
                , (self.vendedor, self.sub_id, self.comprador, self.proveedor, self.proveedor_notas,
                   self.descuento, self.subtotal, self.total, self.comision, self.factura), True)[0]
        # Si no es proveedor, entonces dejamos los campos proveedor y descuento como Null
        else:
            self.id = post(
                '''INSERT INTO venta(vendedor,comprador, sub_id,subtotal,total,comision,proveedor_notas, factura) VALUES(%s,%s,%s,%s,%s,%s,%s, %s) RETURNING 
                id'''
                , (self.vendedor, self.comprador, self.sub_id, self.subtotal, self.total, self.comision,
                   self.proveedor_notas, self.factura)
                , True
            )[0]
        # Verificamos que la venta madre se haya generado adecuadamente
        existe = get('''SELECT * FROM venta WHERE id = %s''', (self.id,), True)
        if len(existe) == 0:
            raise Exception('Ocurrió un error inesperado, por favor vuelva a crear el pedido')

        for producto in self.productos:
            for i in range(producto['cantidad']):
                post('''INSERT INTO producto_venta(producto, venta) VALUES (%s,%s)''', (producto['sku'], self.id),
                     False)
            post('''UPDATE producto SET disponibles = disponibles-%s WHERE sku = %s''',
                 (producto['cantidad'], producto['sku']), False)

        hoy = datetime.datetime.now()
        hoy = hoy.strftime("%d/%m/%Y")
        existe_registro = post(('''UPDATE comisiones SET monto = monto+%s WHERE vendedor = %s and TO_CHAR(fecha,
               'DD/MM/YYYY') = %s RETURNING id'''), (self.comision, self.vendedor, hoy), True)
        if not existe_registro:
            post('''insert into comisiones(vendedor,monto,pagado) values (%s,%s,false)''',
                 (self.vendedor, self.comision), False)
        self.obtener_subid(True)

    @classmethod
    def exist(cls, id):

        """
        Método que verifica si una venta existe

        Parameters:
        * id: el id de la venta

        Returns:

        True si el la venta existe
        """
        exist = get('''SELECT * FROM venta WHERE id = %s''', (id,))

        return exist

    def load(self, params):

        self.id = params['id']
        if not self.exist(self.id):
            raise Exception('No hay venta con el id proporcionado')
        self.id, self.vendedor, self.sub_id, self.estatus, self.comprador, self.proveedor, self.proveedor_notas, self.descuento, self.subtotal, self.total, self.comision, self.fecha, self.factura = get(
            '''SELECT * FROM venta WHERE id = %s''', (self.id,), False)
        if self.proveedor:
            self.comprador = get('''SELECT nombre FROM distribuidores WHERE id = %s''',(self.proveedor,),False)[0]
            self.proveedor = True
        else:
            self.proveedor = False
            self.subtotal = round(self.total / 0.8, 2)
            self.descuento = self.subtotal - self.total

        self.productos = get('''SELECT producto FROM producto_venta WHERE venta = %s''', (self.id,), True)

        self.fecha = self.fecha.strftime("%d/%m/%Y %H:%M:%S")
        if self.estatus == 'pagado' or self.estatus == 'entregado':
            metodos = get('''select distinct jsonb_agg(jsonb_build_object(
            'method', m.nombre,
            'amount', p.cantidad
            )) res FROM venta as v
            INNER JOIN paymentmethod_venta as p
            ON v.id = p.venta
            INNER JOIN paymentmethod as m
            ON m.id = p.method
            WHERE venta = %s
            GROUP BY v.id, m.nombre,p.id''', (self.id,))
            self.metodos = []
            for metodo in metodos:
                self.metodos.append(metodo[0][0])

        diferentes = get('''SELECT producto FROM producto_venta WHERE venta = %s GROUP BY producto''', (self.id,), True)
        for i in range(len(diferentes)):
            sku = diferentes[i][0]

            # si no es proveedor, se regresa el precio con descuento
            if not self.proveedor:
                nombre, precio_descuento = get('''SELECT nombre, precio_descuento FROM producto WHERE sku = %s ''', (sku,), False)

                cantidad = \
                    get('''SELECT COUNT(producto) FROM producto_venta WHERE producto = %s and venta = %s''',
                        (sku, self.id),
                        False)[0]
                self.detalles_productos.append({'nombre': nombre, 'sku': sku, 'precio': precio_descuento, 'cantidad': cantidad,
                                                'total_producto': cantidad * precio_descuento})
            else:
                nombre, precio_lista = get('''SELECT nombre, precio_lista FROM producto WHERE sku = %s ''', (sku,), False)

                cantidad = \
                    get('''SELECT COUNT(producto) FROM producto_venta WHERE producto = %s and venta = %s''',
                        (sku, self.id),
                        False)[0]
                self.detalles_productos.append({'nombre': nombre, 'sku': sku, 'precio': precio_lista, 'cantidad': cantidad,
                                                'total_producto': cantidad * precio_lista})

    @classmethod
    def cancelar_venta(cls, params):
        id = params['id']
        if not cls.exist(id):
            raise Exception('No hay venta con el id proporcionado')
        pagado = get('''SELECT estatus FROM venta WHERE id = %s''', (id,), False)[0]
        if pagado == 'pagado':
            raise Exception('La venta ya había sido pagada')
        elif pagado == 'cancelado':
            raise Exception('La venta ya había sido cancelada')
        post('''UPDATE venta SET estatus = 'cancelado' WHERE id = %s''', (id,), False)

        # Agregamos los productos cancelados a los disponibles
        registros = get('''SELECT producto, COUNT(producto) FROM producto_venta WHERE venta = %s GROUP BY (producto)''',
                        (id,), True)
        for i in range(len(registros)):
            post('''DELETE FROM producto_venta WHERE producto = %s AND venta = %s ''', (registros[i][0], id), False)
            post('''UPDATE producto SET disponibles = disponibles+%s WHERE sku = %s''',
                 (registros[i][1], registros[i][0]), False)

        # Restamos la comision generada por la venta cancelada
        registros = get('''SELECT comision, vendedor FROM venta WHERE id = %s''', (id,), False)
        post('''UPDATE comisiones SET monto = monto-%s WHERE vendedor = %s''', (registros[0], registros[1]), False)

        return f'Venta cancelada exitosamente'

    def calcular_subtotal(self):

        suma = 0

        for producto in self.productos:

            if self.proveedor:
                precio_lista = get('''SELECT precio_lista FROM producto WHERE sku = %s''', (producto['sku'],), False)[0]

                suma += precio_lista * producto['cantidad']
            else:
                precio_descuento = get('''SELECT precio_descuento FROM producto WHERE sku = %s''', (producto['sku'],), False)[0]

                suma += precio_descuento * producto['cantidad']

        return round(suma, 2)

    def calcular_total(self):
        if self.proveedor:
            # Sacamos la cantidad de descuento que le corresponde a ese proveedor
            distribuidor = Distribuidor({"id": self.proveedor})
            self.descuento = distribuidor.descuento
            self.descuento = round(self.subtotal * (self.descuento / 100), 2)
            total = self.subtotal - self.descuento
            return total
        else:
            self.total = self.subtotal
            self.subtotal = round(self.total / 0.8, 2)
            self.descuento = round(self.subtotal - self.total, 2)
            return self.total

    def obtener_subid(self, add=False):
        global primera_venta
        anterior = primera_venta
        if add:
            primera_venta += 1
        return primera_venta

    @classmethod
    def pagar_venta(cls, params):
        metodos = cls.getMethods()
        id = params['id']
        # metodos de pago q usa el usuario
        metodos_pago = params['metodos']
        pagado, total = get('''SELECT estatus, total FROM venta WHERE id = %s''', (id,), False)
        if not cls.exist(id):
            raise Exception('No hay venta con el id proporcionado')
        elif pagado == 'pagado':
            raise Exception('La venta ya había sido pagada')
        elif pagado == 'cancelado':
            raise Exception('La venta ya había sido cancelada')
        amount = 0
        for metodo in metodos_pago:
            amount += metodo['cantidad']
            if metodo['id'] not in metodos:
                raise Exception('Métodos de pago inválidos')
        if amount < total:
            raise Exception('Falta dinero.')
        if amount > total:
            raise Exception('Se está cobrando de más al cliente.')
        for metodo in metodos_pago:
            if metodo['id'] in metodos:
                post('''INSERT INTO paymentmethod_venta(venta, method,cantidad) VALUES(%s, %s, %s)''',
                     (id, metodo['id'], metodo['cantidad']), False)
        post('''UPDATE venta SET estatus = 'pagado' WHERE id = %s''', (id,), False)

    @classmethod
    def entregar_venta(cls, params):
        id = params['id']
        entregado = get('''SELECT estatus FROM venta WHERE id = %s''', (id,), False)[0]
        if not cls.exist(id):
            raise Exception('No hay venta con el id proporcionado')
        elif entregado == 'entregado':
            raise Exception('La venta ya había sido entregada')
        post('''UPDATE venta SET estatus = 'entregado' WHERE id = %s''', (id,), False)

    @classmethod
    def fechas_venta(cls):
        fechas = []
        registros = get('''SELECT TO_CHAR(fecha, 'DD/MM/YYYY') FROM comisiones GROUP BY TO_CHAR(fecha, 'DD/MM/YYYY')''',
                        (), True)
        if not registros:
            raise Exception('No hay ventas registradas en la base de datos')
        for i in range(len(registros)):
            fechas.append(registros[i][0])
        return fechas

    @classmethod
    def registros_dia(cls, params):
        ventas = []
        top3 = []
        total_debito = 0
        total_distribuidor = 0
        total_credito = 0
        total_transferencia = 0
        total_efectivo = 0
        registros = get('''SELECT id FROM venta WHERE TO_CHAR(fecha, 
        'DD/MM/YYYY') = %s AND (estatus = 'entregado' OR estatus = 'pagado')  ''', (params['fecha'],), True)
        if not registros:
            raise Exception('No hay ventas registradas para la fecha seleccionada')

        for i in range(len(registros)):
            venta = Venta({'id': registros[i][0]})

            ventas.append(
                {'id': venta.id, 'total': venta.total, 'comprador': venta.comprador,
                 'vendedor': venta.vendedor, 'metodos_pago': venta.metodos})

            for j in range(len(venta.metodos)):
                if venta.metodos[j]["method"] == 'Crédito proveedor':
                    total_distribuidor += venta.metodos[j]["amount"]
                if venta.metodos[j]["method"] == 'Transferencia':
                    total_transferencia += venta.metodos[j]["amount"]
                if venta.metodos[j]["method"] == 'Efectivo':
                    total_efectivo += venta.metodos[j]["amount"]
                if venta.metodos[j]["method"] == 'Tarjeta de crédito':
                    total_credito += venta.metodos[j]["amount"]
                if venta.metodos[j]["method"] == 'Tarjeta de débito':
                    total_debito += venta.metodos[j]["amount"]

        registros = get('''SELECT producto, count(producto) FROM producto_venta WHERE venta IN (SELECT ID FROM venta WHERE TO_CHAR(fecha, 
        'DD/MM/YYYY') = %s AND (estatus = 'entregado' OR estatus = 'pagado')) GROUP BY producto ORDER BY COUNT(producto) DESC LIMIT 3''', (params['fecha'],),True)
        for i in range(len(registros)):
            top3.append({'producto': registros[i][0], 'cantidad': registros[i][1]})
        return {'ventas': ventas, 'numero_ventas': len(registros), 'total_debito': total_debito,
                'total_credito': total_credito, 'total_distribuidor': total_distribuidor,
                'total_transferencia': total_transferencia, 'total_efectivo': total_efectivo, 'top3': top3}

    @classmethod
    def comisiones_dia(cls, params):
        fecha = params['fecha']
        comisiones = []
        registros = get('''SELECT a.vendedor, sum(b.total), sum(b.comision), a.pagado FROM comisiones as a INNER JOIN 
        venta as b ON TO_CHAR(a.fecha, 'DD/MM/YYYY') = %s and TO_CHAR(b.fecha, 'DD/MM/YYYY') = %s GROUP BY 
        a.vendedor, a.pagado''', (fecha, fecha), True)

        for i in range(len(registros)):
            comisiones.append(
                {'vendedor': registros[i][0], 'total_ventas': registros[i][1], 'comision': registros[i][2],
                 'pagado': registros[i][3]})

        return comisiones

    @classmethod
    def cobrador_pedidos(cls):
        pedidos = []
        registros = get(
            """SELECT id,sub_id,comprador,proveedor,subtotal,descuento,total FROM venta WHERE estatus = 'creado' order by id""",
            (),
            True)
        if not registros:
            raise Exception('No hay pagos pendientes')

        # Si es proveedor, entonces asignamos su nombre a la variable comprador
        for i in range(len(registros)):
            if type(registros[i][3]) == int:
                comprador = registros[i][3]
                proveedor = True
                comprador = get("""SELECT nombre FROM distribuidores WHERE id = %s""", (comprador,), False)[0]
            else:
                proveedor = False
                comprador = registros[i][2]

            venta = Venta({'id': registros[i][0]})

            productos = []
            for j in range(len(venta.detalles_productos)):
                productos.append({'nombre': venta.detalles_productos[j]['nombre'],
                                  'cantidad': venta.detalles_productos[j]['cantidad'],
                                  'total_producto': venta.detalles_productos[j]['total_producto']})
            pedidos.append(
                {'id': registros[i][0], 'sub_id': registros[i][1], 'comprador': comprador, 'proveedor': proveedor,
                 'subtotal': registros[i][4],
                 'descuento': registros[i][5], 'total': registros[i][6], 'productos': productos})

        return pedidos

    @classmethod
    def detalles_pedido(cls, params):
        id = params['id']
        registros = get("""SELECT id FROM venta WHERE id = %s AND (estatus = 'pagado' OR estatus = 'entregado') """,
                        (id,), True)

        if not registros:
            raise Exception('No hay venta con el id proporcionado')

        venta = Venta({'id': id})

        nombre = get('''SELECT nombre FROM usuario WHERE username = %s''', (venta.vendedor,), False)[0]

        productos = []
        for j in range(len(venta.detalles_productos)):
            productos.append({'nombre': venta.detalles_productos[j]['nombre'],
                              'sku': venta.detalles_productos[j]['sku'],
                              'precio': venta.detalles_productos[j]['precio'],
                              'cantidad': venta.detalles_productos[j]['cantidad'],
                              'total_producto': venta.detalles_productos[j]['total_producto']})
        detalles = (
            {'id': venta.id, 'comprador': venta.comprador, 'vendedor': nombre,
             'username': venta.vendedor, 'proveedor': venta.proveedor, 'notas': venta.proveedor_notas,
             'subtotal': venta.subtotal, 'descuento': venta.descuento, 'total': venta.total, 'productos': productos,
             'metodos_pago': venta.metodos, 'factura': venta.factura})
        return detalles

    @classmethod
    def entregador_pedidos(cls):
        pedidos = []
        registros = get(
            """SELECT id,sub_id,comprador,proveedor FROM venta WHERE estatus = 'pagado' order by id""",
            (),
            True)
        if not registros:
            raise Exception('No hay pedidos pendientes de entregar')

        # Si es proveedor, entonces asignamos su nombre a la variable comprador
        for i in range(len(registros)):
            if type(registros[i][3]) == int:
                comprador = registros[i][3]
                proveedor = True
                comprador = get("""SELECT nombre FROM distribuidores WHERE id = %s""", (comprador,), False)[0]
            else:
                proveedor = False
                comprador = registros[i][2]

            venta = Venta({'id': registros[i][0]})

            productos = []
            for j in range(len(venta.detalles_productos)):
                productos.append({'nombre': venta.detalles_productos[j]['nombre'],
                                  'sku': venta.detalles_productos[j]['sku'],
                                  'cantidad': venta.detalles_productos[j]['cantidad']})
            pedidos.append(
                {'id': registros[i][0], 'sub_id': registros[i][1], 'comprador': comprador, 'proveedor': proveedor,
                 'productos': productos})

        return pedidos

    @classmethod
    def fechas_evento(cls, params):
        reciente = params['reciente']
        pagos = params['pagos']
        fechas = []
        ORDER_BY = 'DESC' if reciente else 'ASC'
        if pagos == 'normal':
            QUERY = '''SELECT TO_CHAR(ve.fecha, 'DD/MM/YYYY'), sum(ve.total), count(ve.fecha), b.pagado FROM 
                public.venta AS ve INNER JOIN public.comisiones AS b ON (TO_CHAR(ve.fecha, 'DD/MM/YYYY') = 
                TO_CHAR(b.fecha, 'DD/MM/YYYY')) GROUP BY TO_CHAR(ve.fecha, 'DD/MM/YYYY'), b.pagado ORDER BY 
                TO_CHAR(ve.fecha, 'DD/MM/YYYY') ''' + ORDER_BY
            registros = get(QUERY,
                            (), True)

            if not registros:
                raise Exception('No hay registros en la base de datos')
            for i in range(len(registros)):
                fechas.append({'fecha': registros[i][0], 'total': registros[i][1], 'ventas': registros[i][2],
                               'pagado': registros[i][3]})
        elif pagos == 'pendiente':
            QUERY = '''SELECT TO_CHAR(ve.fecha, 'DD/MM/YYYY'), sum(ve.total), count(ve.fecha), b.pagado FROM 
            public.venta AS ve INNER JOIN public.comisiones AS b ON (TO_CHAR(ve.fecha, 'DD/MM/YYYY') = TO_CHAR(
            b.fecha, 'DD/MM/YYYY')) WHERE b.pagado = false GROUP BY TO_CHAR(ve.fecha, 'DD/MM/YYYY'), b.pagado ORDER 
            BY TO_CHAR(ve.fecha, 'DD/MM/YYYY')  ''' + ORDER_BY
            registros = get(QUERY, (), True)
            if not registros:
                raise Exception('No hay registros en la base de datos')
            for i in range(len(registros)):
                fechas.append({'fecha': registros[i][0], 'total': registros[i][1], 'ventas': registros[i][2],
                               'pagado': registros[i][3]})
        elif pagos == 'pagado':
            QUERY = '''SELECT TO_CHAR(ve.fecha, 'DD/MM/YYYY'), sum(ve.total), count(ve.fecha), b.pagado 
            FROM public.venta AS ve INNER JOIN public.comisiones AS b ON (TO_CHAR(ve.fecha, 'DD/MM/YYYY') = 
            TO_CHAR( b.fecha, 'DD/MM/YYYY')) WHERE b.pagado = true GROUP BY TO_CHAR(ve.fecha, 'DD/MM/YYYY'), 
            b.pagado ORDER BY TO_CHAR(ve.fecha, 'DD/MM/YYYY') ''' + ORDER_BY
            registros = get(QUERY, (), True)
            if not registros:
                raise Exception('No hay registros en la base de datos')
            for i in range(len(registros)):
                fechas.append({'fecha': registros[i][0], 'total': registros[i][1], 'ventas': registros[i][2],
                               'pagado': registros[i][3]})
        else:
            raise Exception('Ingresa una opción de filtrado válida')

        return fechas

    def generar_pdf(self):

        nproductos = len(self.detalles_productos)
        productos = self.detalles_productos
        metodos = self.metodos

        def escribir(i, productos, y1y2, lista):

            if len(productos[i]["nombre"]) > 25:
                productos[i]["nombre"] = productos[i]["nombre"][:25]

            lista.append(
                {'name': f'producto{i}', 'type': 'T', 'x1': 20.0, 'y1': y1y2, 'x2': 95.0, 'y2': y1y2,
                 'font': 'helvetica', 'size': 10, 'bold': 0, 'italic': 0, 'underline': 0, 'align': 'L',
                 'text': productos[i]["nombre"], 'priority': 2, 'multiline': True})
            lista.append(
                {'name': f'sku{i}', 'type': 'T', 'x1': 20.0, 'y1': y1y2 + 3.0, 'x2': 50.0, 'y2': y1y2 + 5.0,
                 'font': 'helvetica',
                 'size': 8, 'bold': 0, 'italic': 0, 'underline': 0, 'align': 'L',
                 'text': productos[i]["sku"],
                 'priority': 2, 'multiline': False})
            lista.append(
                {'name': f'precio{i}', 'type': 'T', 'x1': 95.0, 'y1': y1y2, 'x2': 120.0, 'y2': y1y2,
                 'font': 'helvetica', 'size': 11, 'bold': 0, 'italic': 0, 'underline': 0, 'align': 'L',
                 'text': str('${:.2f}'.format(productos[i]["precio"])), 'priority': 2, 'multiline': False})
            lista.append(
                {'name': f'cantidad{i}', 'type': 'T', 'x1': 144.0, 'y1': y1y2, 'x2': 165.0, 'y2': y1y2,
                 'font': 'helvetica', 'size': 11, 'bold': 0, 'italic': 0, 'underline': 0, 'align': 'L',
                 'text': str(productos[i]["cantidad"]), 'priority': 2, 'multiline': False})
            lista.append(
                {'name': f'total{i}', 'type': 'T', 'x1': 175.0, 'y1': y1y2, 'x2': 200.0, 'y2': y1y2,
                 'font': 'helvetica', 'size': 11, 'bold': 0, 'italic': 0, 'underline': 0, 'align': 'L',
                 'text': str('${:.2f}'.format(productos[i]["total_producto"])), 'priority': 2, 'multiline': False})

        def subtemplate_override(f):

            f["subtotal"] = 'SUBTOTAL:'
            f["monto_descuento"] = str('${:.2f}'.format(self.descuento))
            f["monto_subtotal"] = str('${:.2f}'.format(self.subtotal))

            f["monto_total"] = str('${:.2f}'.format(self.total))

            if self.proveedor:
                f["distribuidor"] = f'NOMBRE DEL DISTRIBUIDOR:'
                f["distribuidor_nombre"] = self.comprador

            else:
                f["distribuidor"] = f'NOMBRE DEL CLIENTE:'
                f["distribuidor_nombre2"] = self.comprador

            f["id_valor"] = str(f'#{self.id}')

            if len(self.metodos) == 1:
                f["metodo_texto"] = '{}: ${:.2f}'.format(self.metodos[0]["method"], self.metodos[0]["amount"])
            elif len(self.metodos) == 2:
                f["metodo_texto"] = '{}: ${:.2f}'.format(self.metodos[0]["method"], self.metodos[0]["amount"])
                f["metodo_texto2"] = '{}: ${:.2f}'.format(self.metodos[1]["method"], self.metodos[1]["amount"])
            elif len(self.metodos) == 3:
                f["metodo_texto"] = '{}: ${:.2f}'.format(self.metodos[0]["method"], self.metodos[0]["amount"])
                f["metodo_texto2"] = '{}: ${:.2f}'.format(self.metodos[1]["method"], self.metodos[1]["amount"])
                f["metodo_texto3"] = '{}: ${:.2f}'.format(self.metodos[2]["method"], self.metodos[2]["amount"])
            elif len(self.metodos) == 3:
                f["metodo_texto"] = '{}: ${:.2f}'.format(self.metodos[0]["method"], self.metodos[0]["amount"])
                f["metodo_texto2"] = '{}: ${:.2f}'.format(self.metodos[1]["method"], self.metodos[1]["amount"])
                f["metodo_texto3"] ='{}: ${:.2f}'.format(self.metodos[2]["method"], self.metodos[2]["amount"])
                f["metodo_texto4"] = '{}: ${:.2f}'.format(self.metodos[3]["method"], self.metodos[3]["amount"])

        pdf = FPDF(format='letter')
        y1y2 = 70.0

        if nproductos < 16:

            elements = template.copy()
            pdf.add_page()
            for i in range(nproductos):
                escribir(i, productos, y1y2, elements)
                y1y2 += 10.0
            temp1 = FlexTemplate(pdf, elements=elements)
            temp2 = FlexTemplate(pdf, elements=subtemplate)
            temp1["title"] = "RESUMEN DE TU COMPRA"
            temp1["company_logo"] = "Global/Utils/logo.png"
            temp1["fecha"] = self.fecha
            temp1["subid_valor"] = str(f'#{self.sub_id}')
            temp1.render()
            subtemplate_override(temp2)
            temp2.render()
            pdf.output("./recibos/" + str(self.id) + ".pdf")
        elif 15 < nproductos < 33:
            elements = template.copy()
            pdf.add_page()
            for i in range(17):
                escribir(i, productos, y1y2, elements)
                y1y2 += 10.0
            temp1 = FlexTemplate(pdf, elements=elements)
            temp1["title"] = "RESUMEN DE TU COMPRA"
            temp1["company_logo"] = "Global/Utils/logo.png"
            temp1["fecha"] = self.fecha
            temp1["subid_valor"] = str(f'#{self.sub_id}')
            temp1.render()
            pdf.add_page()
            elements2 = elements[:9]
            y1y2 = 70.0
            for i in range(17, nproductos):
                escribir(i, productos, y1y2, elements2)
                y1y2 += 10.0

            temp2 = FlexTemplate(pdf, elements=elements2)
            temp3 = FlexTemplate(pdf, elements=subtemplate)
            temp2["title"] = "RESUMEN DE TU COMPRA"
            temp2["company_logo"] = "Global/Utils/logo.png"
            temp2["fecha"] = self.fecha
            temp2["subid_valor"] = str(f'#{self.sub_id}')
            subtemplate_override(temp3)
            temp2.render()
            temp3.render()
            pdf.output("./recibos/" + str(self.id) + ".pdf")
        elif 32 < nproductos < 50:
            elements = template.copy()
            pdf.add_page()
            for i in range(17):
                escribir(i, productos, y1y2, elements)
                y1y2 += 10.0
            temp1 = FlexTemplate(pdf, elements=elements)
            temp1["title"] = "RESUMEN DE TU COMPRA"
            temp1["company_logo"] = "Global/Utils/logo.png"
            temp1["fecha"] = self.fecha
            temp1["subid_valor"] = str(f'#{self.sub_id}')
            temp1.render()
            pdf.add_page()
            elements2 = elements[:9]
            y1y2 = 70.0
            for i in range(17, 34):
                escribir(i, productos, y1y2, elements2)
                y1y2 += 10.0

            temp2 = FlexTemplate(pdf, elements=elements2)
            temp2["title"] = "RESUMEN DE TU COMPRA"
            temp2["company_logo"] = "Global/Utils/logo.png"
            temp2["fecha"] = self.fecha
            temp2["subid_valor"] = str(f'#{self.sub_id}')
            temp2.render()
            pdf.add_page()
            elements3 = elements[:9]
            y1y2 = 70.0
            for i in range(34, nproductos):
                escribir(i, productos, y1y2, elements3)
                y1y2 += 10.0

            temp3 = FlexTemplate(pdf, elements=elements3)
            temp4 = FlexTemplate(pdf, elements=subtemplate)
            temp3["title"] = "RESUMEN DE TU COMPRA"
            temp3["company_logo"] = "Global/Utils/logo.png"
            temp3["fecha"] = self.fecha
            temp3["subid_valor"] = str(f'#{self.sub_id}')
            subtemplate_override(temp4)
            temp3.render()
            temp4.render()

            pdf.output("./recibos/" + str(self.id) + ".pdf")
        else:
            raise Exception('Esta venta tiene demasiados productos.')

    @classmethod
    def reporte(cls, params):
        ventas = get('''SELECT * FROM producto WHERE estatus = True''', ())
        ventas_producto = get('''select COUNT(*), producto from producto_venta as pv WHERE pv.venta in (SELECT id 
        from venta WHERE estatus='entregado' AND TO_CHAR(fecha, 'DD/MM/YYYY') in (select TO_CHAR(fecha, 'DD/MM/YYYY') 
        from venta order by id desc limit 1) )  GROUP BY producto ''', ())
        productos = {}
        for venta in ventas_producto:
            productos[venta[1]] = venta[0]
        import pandas as pd
        info = {
            "codigo": [],
            "nombre": [],
            "precio al publico": [],
            "precio a distribuidor": [],
            "inventario inicial": [],
            "numero de ventas": [],
            "inventario restante": []
        }

        for venta in ventas:
            info['codigo'].append(venta[6])
            info['nombre'].append(venta[1])
            info['precio al publico'].append(venta[2])
            info['precio a distribuidor'].append(venta[3])
            info['inventario inicial'].append(venta[5])
            info['numero de ventas'].append(productos.get(venta[6], 0))
            # info['numero de ventas'].append(ventas[0])
            info['inventario restante'].append(venta[4])

        df = pd.DataFrame(info)
        df.sort_values(by=['codigo'])
        if params['path'][-5:] == '.xlsx':
            df.to_excel(params['path'], index=False)
        else:
            df.to_excel(params['path'] + '.xlsx', index=False)
        return 'Se ha guardado el reporte en ' + params['path']

    @classmethod
    def getMethods(cls):
        metodos = get('''SELECT * FROM paymentmethod''', ())
        methods = {}
        for method in metodos:
            methods[method[0]] = {
                "id": method[0],
                "nombre": method[1]
            }
        return methods

    @classmethod
    def facturas_pendientes(cls):
        ventas = []
        registros = get('''SELECT * FROM venta WHERE factura = true''',(),True)
        if not registros:
            raise Exception('No hay facturas pendientes')
        for i in range(len(registros)):
            ventas.append({'id': registros[i][0], 'vendedor': registros[i][1], 'sub_id': registros[i][2],
                           'estatus': registros[i][3], 'comprador': registros[i][4], 'proveedor': registros[i][5],
                           'notas': registros[i][6], 'descuento': registros[i][7], 'subtotal': registros[i][8],
                           'total': registros[i][9], 'comision': registros[i][10],
                           'fecha': registros[i][11].strftime("%d/%m/%Y %H:%M:%S"), 'factura': registros[i][12]})

        return ventas

    @classmethod
    def facturas_facturar(cls, params):
        exist = get('''SELECT factura FROM venta where id = %s''', (params['id'],), False)

        if not exist:
            raise Exception('No hay ventas con el id proporcionado')
        elif not exist[0]:
            raise Exception('No se requiere factura para esta venta')

        post('''UPDATE venta SET factura = false WHERE id = %s''', (params['id'],), False)

        return f'El estado de la factura se cambió exitosamente'

    @classmethod
    def editar_proveedor(cls, params):
        exist = get('''SELECT id FROM distribuidores WHERE id = %s''',(params['id'],), False)
        if not exist:
            raise Exception('No hay proveedor registrado con ese id')

        if params["nombre"]:
            post('''UPDATE distribuidores SET nombre = %s WHERE id = %s''',(params["nombre"],params["id"]), False)
        if params["descuento"]:
            post('''UPDATE distribuidores SET descuento = %s WHERE id = %s''', (params["descuento"], params["id"]), False)

        if params["activo"] == False:
            post('''UPDATE distribuidores SET activo = false WHERE id = %s''', (params["id"],),False)
        elif params["activo"] == True:
            post('''UPDATE distribuidores SET activo = true WHERE id = %s''', (params["id"],), False)

        return f'El proveedor se editó correctamente'

