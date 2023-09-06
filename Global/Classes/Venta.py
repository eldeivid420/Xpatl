import json

from Global.Utils.db import post, get
import datetime
from fpdf import FPDF, FlexTemplate


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
                'font': 'helvetica', 'size': 12, 'bold': 0, 'italic': 0, 'underline': 0, 'align': 'L','text': '',
                'priority': 2, 'multiline': True},

               {'name': 'subtotal', 'type': 'T', 'x1': 20.0, 'y1': 240.0, 'x2': 65.0, 'y2': 240.0, 'font': 'helvetica',
                'size': 12, 'bold': 1, 'italic': 0, 'underline': 0, 'align': 'L', 'text': '', 'priority': 2,
                'multiline': False},
               {'name': 'monto_subtotal', 'type': 'T', 'x1': 65.0, 'y1': 240.0, 'x2': 105.0, 'y2': 240.0,
                'font': 'helvetica', 'size': 12, 'bold': 0, 'italic': 0, 'underline': 0, 'align': 'L',
                'text': '', 'priority': 2, 'multiline': False},

               {'name': 'subtotal2', 'type': 'T', 'x1': 20.0, 'y1': 245.0, 'x2': 65.0, 'y2': 245.0, 'font': 'helvetica',
                'size': 12, 'bold': 1, 'italic': 0, 'underline': 0, 'align': 'L', 'text': '', 'priority': 2,
                'multiline': False},
               {'name': 'monto_subtotal2', 'type': 'T', 'x1': 65.0, 'y1': 244.0, 'x2': 105.0, 'y2': 244.0,
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

               {'name': 'id', 'type': 'T', 'x1': 100.0, 'y1': 245.0, 'x2': 130.0, 'y2': 245.0,
                'font': 'helvetica', 'size': 12, 'bold': 1, 'italic': 0, 'underline': 0, 'align': 'L',
                'text': 'FOLIO:', 'priority': 2, 'multiline': False},
               {'name': 'id_valor', 'type': 'T', 'x1': 115.0, 'y1': 245.0, 'x2': 150.0, 'y2': 245.0,
                'font': 'helvetica', 'size': 12, 'bold': 0, 'italic': 0, 'underline': 0, 'align': 'L',
                'text': '', 'priority': 2, 'multiline': False},

               {'name': 'metodo', 'type': 'T', 'x1': 100.0, 'y1': 255.0, 'x2': 150.0, 'y2': 255.0, 'font': 'helvetica',
                'size': 12, 'bold': 1, 'italic': 0, 'underline': 0, 'align': 'L', 'text': 'MÉTODO DE PAGO:',
                'priority': 2, 'multiline': False},
               {'name': 'metodo_texto', 'type': 'T', 'x1': 143.0, 'y1': 255.0, 'x2': 220.0, 'y2': 255.0,
                'font': 'helvetica', 'size': 12, 'bold': 0, 'italic': 0, 'underline': 0, 'align': 'L',
                'text': '', 'priority': 2, 'multiline': False}]


class Venta:

    def __init__(self, params, load=True):
        self.id = None
        self.vendedor = None
        self.sub_id = None
        self.tipo = None
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
        self.load(params) if load else self.create(params)

    def create(self, params):

        # TODO: implementar funcion que genere sub_id usando el timestamp de la base de datos

        self.vendedor = params['vendedor']
        self.sub_id = self.obtener_subid()
        self.comprador = params['comprador']
        self.proveedor = params['proveedor']
        self.proveedor_notas = params['proveedor_notas']
        self.descuento = params['descuento']
        self.productos = params['productos']
        self.subtotal = self.calcular_subtotal()
        self.total = self.calcular_total()
        self.comision = (self.subtotal * 0.8) * 0.1
        if len(self.productos) == 0:
            raise Exception('No puedes generar una venta vacía')

        productos_agotados = []
        productos_insuficientes = []

        for producto in self.productos:
            disponible, nombre, sku = get('''SELECT disponibles, nombre, sku FROM producto WHERE sku = %s''', (producto['sku'],),
                                     False)
            #print(f'NOMBRE {nombre}  DISP: {disponible}')
            if disponible == 0:
                productos_agotados.append(sku)
            elif disponible < producto['cantidad']:
                productos_insuficientes.append({'sku': sku, 'disponibles': disponible})

        if len(productos_agotados) != 0 or len(productos_insuficientes) != 0:
            info = {'productos_insuficientes': productos_insuficientes, 'productos_agotados': productos_agotados}
            raise Exception(json.dumps(info))

        # Verificamos si es una venta para un proveedor
        if self.proveedor and self.descuento:
            self.comision = 0
            self.id = post(
                '''INSERT INTO venta(vendedor,sub_id,comprador,proveedor,proveedor_notas,descuento,subtotal,total,comision) 
                VALUES(%s, %s,%s,%s,%s,%s,%s,%s,%s) RETURNING id'''
                , (self.vendedor, self.sub_id, self.comprador, self.proveedor, self.proveedor_notas,
                   self.descuento, self.subtotal, self.total, self.comision), True)[0]
        # Si no es proveedor, entonces dejamos los campos proveedor y descuento como Null
        else:
            self.id = post(
                '''INSERT INTO venta(vendedor,comprador, sub_id,subtotal,total,comision,proveedor_notas) VALUES(%s,%s,%s,%s,%s,%s,%s) RETURNING 
                id'''
                , (self.vendedor, self.comprador, self.sub_id, self.subtotal, self.total, self.comision, self.proveedor_notas)
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
        self.id, self.vendedor, self.sub_id, self.tipo, self.estatus, self.comprador, self.proveedor, self.proveedor_notas, self.descuento, self.subtotal, self.total, self.comision, self.fecha = get(
            '''SELECT * FROM venta WHERE id = %s''', (self.id,), False)
        if self.proveedor:
            self.comprador = self.proveedor
            self.proveedor = True
        else:
            self.proveedor = False

        self.productos = get('''SELECT producto FROM producto_venta WHERE venta = %s''', (self.id,), True)

        self.fecha = self.fecha.strftime("%d/%m/%Y %H:%M:%S")
        self.tipo = params.get('tipo', None)
        diferentes = get('''SELECT producto FROM producto_venta WHERE venta = %s GROUP BY producto''', (self.id,), True)

        for i in range(len(diferentes)):
            sku = diferentes[i][0]

            # si no es proveedor, se regresa el precio especial
            if not self.proveedor:
                nombre, precio = get('''SELECT nombre, precio_esp FROM producto WHERE sku = %s ''', (sku,), False)

                cantidad = \
                    get('''SELECT COUNT(producto) FROM producto_venta WHERE producto = %s and venta = %s''', (sku, self.id),
                        False)[0]
                self.detalles_productos.append({'nombre': nombre, 'sku': sku, 'precio': precio, 'cantidad': cantidad,
                                                'total_producto': cantidad * precio})
            else:
                nombre, precio = get('''SELECT nombre, precio FROM producto WHERE sku = %s ''', (sku,), False)

                cantidad = \
                    get('''SELECT COUNT(producto) FROM producto_venta WHERE producto = %s and venta = %s''', (sku, self.id),
                        False)[0]
                self.detalles_productos.append({'nombre': nombre, 'sku': sku, 'precio': precio, 'cantidad': cantidad,
                                                'total_producto': cantidad * precio})

    @classmethod
    def cancelar_venta(cls, params):
        id = params['id']
        if not cls.exist(id):
            raise Exception('No hay venta con el id proporcionado')
        pagado = get('''SELECT estatus FROM venta WHERE id = %s''',(id,), False)[0]
        if pagado == 'pagado':
            raise Exception('La venta ya había sido pagada')
        elif pagado == 'cancelado':
            raise Exception('La venta ya había sido cancelada')
        post('''UPDATE venta SET estatus = 'cancelado' WHERE id = %s''', (id,), False)

        # Agregamos los productos cancelados a los disponibles
        registros = get('''SELECT producto, COUNT(producto) FROM producto_venta WHERE venta = %s GROUP BY (producto)''', (id,), True)
        for i in range(len(registros)):
            post('''DELETE FROM producto_venta WHERE producto = %s AND venta = %s ''',(registros[i][0], id), False)
            post('''UPDATE producto SET disponibles = disponibles+%s WHERE sku = %s''', (registros[i][1], registros[i][0]), False)

        # Restamos la comision generada por la venta cancelada
        registros = get('''SELECT comision, vendedor FROM venta WHERE id = %s''', (id,), False)
        post('''UPDATE comisiones SET monto = monto-%s WHERE vendedor = %s''', (registros[0], registros[1]), False)

        return f'Venta cancelada exitosamente'

    def calcular_subtotal(self):

        suma = 0

        for producto in self.productos:

            if self.proveedor and self.descuento:
                precio = get('''SELECT precio FROM producto WHERE sku = %s''', (producto['sku'],), False)[0]

                suma += precio * producto['cantidad']
            else:
                precio = get('''SELECT precio_esp FROM producto WHERE sku = %s''', (producto['sku'],), False)[0]

                suma += precio * producto['cantidad']

        return round(suma, 2)

    def calcular_total(self):
        if self.proveedor:
            total = self.subtotal * (self.descuento / 100)
            return round(total, 2)
        else:
            return self.subtotal

    def obtener_subid(self, add=False):
        global primera_venta
        anterior = primera_venta
        if add:
            primera_venta += 1
        return primera_venta

    @classmethod
    def pagar_venta(cls, params):
        tipos = ['efectivo', 'debito', 'credito', 'credito proveedor']
        id = params['id']
        tipo = params['tipo']
        pagado = get('''SELECT estatus FROM venta WHERE id = %s''', (id,), False)[0]
        if not cls.exist(id):
            raise Exception('No hay venta con el id proporcionado')
        elif pagado == 'pagado':
            raise Exception('La venta ya había sido pagada')
        elif tipo not in tipos:
            raise Exception('Ingrese una forma de pago válida')
        elif pagado == 'cancelado':
            raise Exception('La venta ya había sido cancelada')
        post('''UPDATE venta SET tipo = %s, estatus = 'pagado' WHERE id = %s''', (tipo, id), False)

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
    def registgros_dia(cls, params):
        registros = get('''SELECT * FROM venta WHERE TO_CHAR(fecha, 'DD/MM/YYYY') = %s''', (params['fecha'],), True)
        if not registros:
            raise Exception('No hay ventas registradas para la fecha seleccionada')
        ventas = []

        for i in range(len(registros)):
            if registros[i][6]:
                comprador = registros[i][6]
                proveedor = True
            else:
                proveedor = False
                comprador = registros[i][5]
            ventas.append(
                {'id': registros[i][0], 'vendedor': registros[i][1], 'sub_id': registros[i][2], 'tipo': registros[i][3],
                 'estatus': registros[i][4], 'comprador': comprador, 'proveedor': proveedor,
                 'proveedor_notas': registros[i][7],
                 'descuento': registros[i][8], 'subtotal': registros[i][9], 'total': registros[i][10],
                 'comision': registros[i][11], 'fecha': registros[i][12].strftime("%d/%m/%Y")})
        return ventas

    @classmethod
    def cobrador_pedidos(cls):
        pedidos = []
        registros = get(
            """SELECT id,sub_id,comprador,proveedor,subtotal,descuento,total FROM venta WHERE estatus = 'creado' order by id""", (),
            True)
        if not registros:
            raise Exception('No hay pagos pendientes')

        # Si es proveedor, entonces asignamos su nombre a la variable comprador
        for i in range(len(registros)):
            if registros[i][3]:
                comprador = registros[i][3]
                proveedor = True
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
    def entregador_pedidos(cls):
        pedidos = []
        registros = get(
            """SELECT id,sub_id,comprador,proveedor,subtotal,descuento,total FROM venta WHERE estatus = 'pagado' order by id""",
            (),
            True)
        if not registros:
            raise Exception('No hay pedidos pendientes de entregar')

        # Si es proveedor, entonces asignamos su nombre a la variable comprador
        for i in range(len(registros)):
            if registros[i][3]:
                comprador = registros[i][3]
                proveedor = True
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
    def fechas_evento(cls, params):
        reciente = params['reciente']
        pagos = params['pagos']
        fechas = []

        if pagos == 'normal' and reciente:
            registros = get(
                '''SELECT TO_CHAR(ve.fecha, 'DD/MM/YYYY'), sum(ve.total), count(ve.fecha), b.pagado FROM 
                public.venta AS ve INNER JOIN public.comisiones AS b ON (TO_CHAR(ve.fecha, 'DD/MM/YYYY') = 
                TO_CHAR(b.fecha, 'DD/MM/YYYY')) GROUP BY TO_CHAR(ve.fecha, 'DD/MM/YYYY'), b.pagado ORDER BY 
                TO_CHAR(ve.fecha, 'DD/MM/YYYY') DESC''',
                (), True)
            if not registros:
                raise Exception('No hay registros en la base de datos')
            for i in range(len(registros)):
                fechas.append({'fecha': registros[i][0], 'total': registros[i][1], 'ventas': registros[i][2],
                               'pagado': registros[i][3]})
        elif pagos == 'normal' and not reciente:
            registros = get(
                '''SELECT TO_CHAR(ve.fecha, 'DD/MM/YYYY'), sum(ve.total), count(ve.fecha), b.pagado FROM 
                public.venta AS ve INNER JOIN public.comisiones AS b ON (TO_CHAR(ve.fecha, 'DD/MM/YYYY') = 
                TO_CHAR(b.fecha, 'DD/MM/YYYY')) GROUP BY TO_CHAR(ve.fecha, 'DD/MM/YYYY'), b.pagado ORDER BY 
                TO_CHAR(ve.fecha, 'DD/MM/YYYY') ASC''',
                (), True)
            if not registros:
                raise Exception('No hay registros en la base de datos')
            for i in range(len(registros)):
                fechas.append({'fecha': registros[i][0], 'total': registros[i][1], 'ventas': registros[i][2],
                               'pagado': registros[i][3]})
        elif pagos == 'pendiente' and reciente:
            registros = get('''SELECT TO_CHAR(ve.fecha, 'DD/MM/YYYY'), sum(ve.total), count(ve.fecha), b.pagado FROM 
            public.venta AS ve INNER JOIN public.comisiones AS b ON (TO_CHAR(ve.fecha, 'DD/MM/YYYY') = TO_CHAR(
            b.fecha, 'DD/MM/YYYY')) WHERE b.pagado = false GROUP BY TO_CHAR(ve.fecha, 'DD/MM/YYYY'), b.pagado ORDER 
            BY TO_CHAR(ve.fecha, 'DD/MM/YYYY') DESC''', (), True)
            if not registros:
                raise Exception('No hay registros en la base de datos')
            for i in range(len(registros)):
                fechas.append({'fecha': registros[i][0], 'total': registros[i][1], 'ventas': registros[i][2],
                               'pagado': registros[i][3]})
        elif pagos == 'pendiente' and not reciente:
            registros = get('''SELECT TO_CHAR(ve.fecha, 'DD/MM/YYYY'), sum(ve.total), count(ve.fecha), b.pagado FROM 
            public.venta AS ve INNER JOIN public.comisiones AS b ON (TO_CHAR(ve.fecha, 'DD/MM/YYYY') = TO_CHAR(
            b.fecha, 'DD/MM/YYYY')) WHERE b.pagado = false GROUP BY TO_CHAR(ve.fecha, 'DD/MM/YYYY'), b.pagado ORDER 
            BY TO_CHAR(ve.fecha, 'DD/MM/YYYY') ASC''', (), True)
            if not registros:
                raise Exception('No hay registros en la base de datos')
            for i in range(len(registros)):
                fechas.append({'fecha': registros[i][0], 'total': registros[i][1], 'ventas': registros[i][2],
                               'pagado': registros[i][3]})
        elif pagos == 'pagado' and reciente:
            registros = get('''SELECT TO_CHAR(ve.fecha, 'DD/MM/YYYY'), sum(ve.total), count(ve.fecha), b.pagado 
            FROM public.venta AS ve INNER JOIN public.comisiones AS b ON (TO_CHAR(ve.fecha, 'DD/MM/YYYY') = 
            TO_CHAR( b.fecha, 'DD/MM/YYYY')) WHERE b.pagado = true GROUP BY TO_CHAR(ve.fecha, 'DD/MM/YYYY'), 
            b.pagado ORDER BY TO_CHAR(ve.fecha, 'DD/MM/YYYY') DESC''', (), True)
            if not registros:
                raise Exception('No hay registros en la base de datos')
            for i in range(len(registros)):
                fechas.append({'fecha': registros[i][0], 'total': registros[i][1], 'ventas': registros[i][2],
                               'pagado': registros[i][3]})
        elif pagos == 'pagado' and not reciente:
            registros = get('''SELECT TO_CHAR(ve.fecha, 'DD/MM/YYYY'), sum(ve.total), count(ve.fecha), b.pagado 
            FROM public.venta AS ve INNER JOIN public.comisiones AS b ON (TO_CHAR(ve.fecha, 'DD/MM/YYYY') = 
            TO_CHAR( b.fecha, 'DD/MM/YYYY')) WHERE b.pagado = true GROUP BY TO_CHAR(ve.fecha, 'DD/MM/YYYY'), 
            b.pagado ORDER BY TO_CHAR(ve.fecha, 'DD/MM/YYYY') ASC''', (), True)
            if not registros:
                raise Exception('No hay registros en la base de datos')
            for i in range(len(registros)):
                fechas.append({'fecha': registros[i][0], 'total': registros[i][1], 'ventas': registros[i][2],
                               'pagado': registros[i][3]})
        else:
            raise Exception('Ingresa una opción de filtrado válida')

        return fechas




        # filtramos por tipo de pagos


        return fechas


    def generar_pdf(self):

        nproductos = len(self.detalles_productos)
        productos = self.detalles_productos

        def escribir(i, productos, y1y2, lista):

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
                 'text': str(f'${productos[i]["precio"]}'), 'priority': 2, 'multiline': False})
            lista.append(
                {'name': f'cantidad{i}', 'type': 'T', 'x1': 144.0, 'y1': y1y2, 'x2': 165.0, 'y2': y1y2,
                 'font': 'helvetica', 'size': 11, 'bold': 0, 'italic': 0, 'underline': 0, 'align': 'L',
                 'text': str(productos[i]["cantidad"]), 'priority': 2, 'multiline': False})
            lista.append(
                {'name': f'total{i}', 'type': 'T', 'x1': 175.0, 'y1': y1y2, 'x2': 200.0, 'y2': y1y2,
                 'font': 'helvetica', 'size': 11, 'bold': 0, 'italic': 0, 'underline': 0, 'align': 'L',
                 'text': str(f'${round(productos[i]["total_producto"], 2)}'), 'priority': 2, 'multiline': False})

        def subtemplate_override(f):


            if self.descuento:
                f["monto_descuento"] = str(f'${round(float(self.subtotal * (self.descuento / 100.00)), 2)}')
                f["subtotal"] = 'SUBTOTAL:'
                f["monto_subtotal"] = str(f'${round(self.subtotal, 2)}')
            else:
                f["descuento"] = ""
                f["subtotal2"] = 'SUBTOTAL:'
                f["monto_subtotal2"] = str(f'${round(self.subtotal, 2)}')

            f["monto_total"] = str(f'${round(self.total, 2)}')
            if self.proveedor:
                f["distribuidor"] = f'NOMBRE DEL DISTRIBUIDOR:'
                f["distribuidor_nombre"] = self.comprador
            f["id_valor"] = str(f'#{self.id}')
            if self.tipo == 'credito':
                tipo = 'Tarjeta de crédito'
            elif self.tipo == 'debito':
                tipo = 'Tarjeta de débito'
            elif self.tipo == 'credito proveedor':
                tipo = 'A crédito de distribuidor'
            else:
                tipo = 'Efectivo'
            f["metodo_texto"] = tipo

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
            temp1["subid"] = str(f'#{self.sub_id}')
            temp1.render()
            pdf.add_page()
            elements2 = elements[:7]
            y1y2 = 70.0
            for i in range(17, nproductos):
                escribir(i, productos, y1y2, elements2)
                y1y2 += 10.0

            temp2 = FlexTemplate(pdf, elements=elements2)
            temp3 = FlexTemplate(pdf, elements=subtemplate)
            temp2["title"] = "RESUMEN DE TU COMPRA"
            temp2["company_logo"] = "Global/Utils/logo.png"
            temp2["fecha"] = temp1["fecha"]
            temp2["subid"] = temp1["subid"]
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
            temp1["subid"] = str(f'#{self.sub_id}')
            temp1.render()
            pdf.add_page()
            elements2 = elements[:7]
            y1y2 = 70.0
            for i in range(34):
                escribir(i, productos, y1y2, elements2)
                y1y2 += 10.0

            temp2 = FlexTemplate(pdf, elements=elements2)
            temp2["title"] = "RESUMEN DE TU COMPRA"
            temp2["company_logo"] = "Global/Utils/logo.png"
            temp2["fecha"] = temp1["fecha"]
            temp2["subid"] = temp1["subid"]
            temp2.render()
            pdf.add_page()
            elements3 = elements[:7]
            y1y2 = 70.0
            for i in range(34, nproductos):
                escribir(i, productos, y1y2, elements2)
                y1y2 += 10.0
            temp3 = FlexTemplate(pdf, elements=elements3)
            temp4 = FlexTemplate(pdf, elements=subtemplate)
            temp3["title"] = "RESUMEN DE TU COMPRA"
            temp3["company_logo"] = "Global/Utils/logo.png"
            temp3["fecha"] = temp1["fecha"]
            temp3["subid"] = temp1["subid"]
            subtemplate_override(temp4)
            temp3.render()
            temp4.render()

            pdf.output("./recibos/" + str(self.id) + ".pdf")
        else:
            raise Exception('Esta venta tiene demasiados productos.')
