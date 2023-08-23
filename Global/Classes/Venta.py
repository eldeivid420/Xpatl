import json

from Global.Utils.db import post, get
import datetime
from fpdf import Template

# TODO: Documentar
primera_venta = 1


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
        self.comision = (self.subtotal*0.8)*0.1
        if len(self.productos) == 0:
            raise Exception('No puedes generar una venta vacía')
        # Verificamos si es una venta para un proveedor

        if self.proveedor and self.descuento:
            self.id = post(
                '''INSERT INTO venta(vendedor,sub_id,comprador,proveedor,proveedor_notas,descuento,subtotal,total,comision) 
                VALUES(%s, %s,%s,%s,%s,%s,%s,%s,%s) RETURNING id'''
                , (self.vendedor, self.sub_id,self.comprador, self.proveedor, self.proveedor_notas,
                   self.descuento, self.subtotal, self.total,self.comision), True)[0]
        # Si no es proveedor, entonces dejamos los campos proveedor y descuento como Null
        else:
            self.id = post(
                '''INSERT INTO venta(vendedor,comprador, sub_id,subtotal,total,comision) VALUES(%s,%s,%s,%s,%s,%s) RETURNING 
                id'''
                , (self.vendedor,self.comprador, self.sub_id, self.subtotal, self.total, self.comision)
                , True
            )[0]
        for producto in self.productos:
            disponible, nombre = get('''SELECT disponibles, nombre FROM producto WHERE sku = %s''', (producto['sku'],),False)
            if disponible < producto['cantidad']:
                productos_agotados = []
                registros_agotados = get('''SELECT nombre FROM producto WHERE disponibles < 1''',(),True)
                for i in range(len(registros_agotados)):
                    productos_agotados.append(registros_agotados[i][0])
                info = [{'producto': nombre, 'disponibles': disponible}, {'agotados': productos_agotados}]
                raise Exception(json.dumps(info))

            for i in range(producto['cantidad']):
                post('''INSERT INTO producto_venta(producto, venta) VALUES (%s,%s)''', (producto['sku'], self.id),
                     False)
            post('''UPDATE producto SET disponibles = disponibles-%s WHERE sku = %s''', (producto['cantidad'], producto['sku']), False)

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

        for i in range(len(self.productos)):
            sku = self.productos[i][0]
            nombre, precio = get('''SELECT nombre, precio FROM producto WHERE sku = %s ''', (sku,), False)
            cantidad = get('''SELECT COUNT(producto) FROM producto_venta WHERE producto = %s and venta = %s''', (sku, self.id), False)[0]
            self.detalles_productos.append({'nombre': nombre, 'sku': sku, 'precio': precio, 'cantidad': cantidad, 'total_producto': cantidad*precio})



    @classmethod
    def cancelar_venta(cls, params):
        id = params['id']
        if not cls.exist(id):
            raise Exception('No hay venta con el id proporcionado')
        post('''UPDATE venta SET estatus = 'cancelado' WHERE id = %s''', (id,), False)
        return f'Venta cancelada exitosamente'

    def calcular_subtotal(self):

        suma = 0
        for producto in self.productos:
            precio = get('''SELECT precio FROM producto WHERE sku = %s''', (producto['sku'],), False)[0]
            suma += precio*producto['cantidad']

        return round(suma, 2)

    def calcular_total(self):
        if self.proveedor:
            total = self.subtotal * (self.descuento/100)
            return round(total, 2)
        else:
            return self.subtotal

    def obtener_subid(self, add = False):
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
        registros = get('''SELECT TO_CHAR(fecha, 'DD/MM/YYYY') FROM comisiones GROUP BY TO_CHAR(fecha, 'DD/MM/YYYY')''', (), True)
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
                 'estatus': registros[i][4],'comprador': comprador, 'proveedor': proveedor, 'proveedor_notas': registros[i][7],
                 'descuento': registros[i][8], 'subtotal': registros[i][9], 'total': registros[i][10],
                 'comision': registros[i][11], 'fecha': registros[i][12].strftime("%d/%m/%Y")})
        return ventas

    def generar_pdf(self):
        if len(self.detalles_productos) < 7:
            elements = [
                {'name': 'border', 'type': 'B', 'x1': 10.0, 'y1': 10., 'x2': 205.9, 'y2': 269.4},
                {'name': 'company_logo', 'type': 'I', 'x1': 20.0, 'y1': 20.0, 'x2': 65.0, 'y2': 40.0, 'font': None,
                 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 'align': 'L', 'text': 'logo', 'priority': 2,
                 'multiline': False},
                {'name': 'title', 'type': 'T', 'x1': 70.0, 'y1': 55.0, 'x2': 140.0, 'y2': 37.5, 'font': 'helvetica',
                 'size': 12.0, 'bold': 1, 'italic': 0, 'underline': 0, 'align': 'C', 'text': '', 'priority': 2,
                 'multiline': False},
                {'name': 'productos', 'type': 'T', 'x1': 20.0, 'y1': 60.0, 'x2': 50.0, 'y2': 65.0, 'font': 'helvetica',
                 'size': 12, 'bold': 1, 'italic': 0, 'underline': 0, 'align': 'L', 'text': 'PRODUCTOS', 'priority': 2,
                 'multiline': False},
                {'name': 'precios', 'type': 'T', 'x1': 85.0, 'y1': 60.0, 'x2': 130.0, 'y2': 65.0, 'font': 'helvetica',
                 'size': 12, 'bold': 1, 'italic': 0, 'underline': 0, 'align': 'L', 'text': 'PRECIO X UNIDAD', 'priority': 2,
                 'multiline': False},
                {'name': 'cantidades', 'type': 'T', 'x1': 135.0, 'y1': 60.0, 'x2': 165.0, 'y2': 65.0, 'font': 'helvetica',
                 'size': 12, 'bold': 1, 'italic': 0, 'underline': 0, 'align': 'L', 'text': 'CANTIDAD', 'priority': 2,
                 'multiline': False},
                {'name': 'totales', 'type': 'T', 'x1': 175.0, 'y1': 60.0, 'x2': 195.0, 'y2': 65.0, 'font': 'helvetica',
                 'size': 12, 'bold': 1, 'italic': 0, 'underline': 0, 'align': 'L', 'text': 'TOTAL', 'priority': 2,
                 'multiline': False}
            ]
            # here we instantiate the template
            f = Template(format="letter", elements=elements,
                         title="Sample Invoice")
            f.add_page()

            # we FILL some of the fields of the template with the information we want
            # note we access the elements treating the template instance as a "dict"
            f["title"] = "RESUMEN DE TU COMPRA"
            f["company_logo"] = "tutorial/logo.png"

            # and now we render the page
            f.render("./template.pdf")
        elif len(self.detalles_productos) > 7:
            pass


