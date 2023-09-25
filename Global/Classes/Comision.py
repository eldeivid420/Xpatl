from Global.Utils.db import post, get
import datetime


class Comision:

    def __init__(self, params):
        self.id = None
        self.vendedor = None
        self.monto = None
        self.pagado = None
        self.fecha = None
        self.pagado = None
        self.pagado_en = None
        self.load(params)

    def load(self, params):
        self.id = params['id']
        existe = get('''SELECT id FROM comisiones WHERE id = %s''', (self.id,), False)
        if not existe:
            raise Exception('No existe ninguna comisión con ese id')
        self.vendedor, self.monto, self.pagado, self.pagado_en = get('''SELECT vendedor, monto, pagado, pagado_en FROM 
        comisiones WHERE id = %s''', (self.id, ), False)

    @classmethod
    def buscar_comisiones_fecha(cls, params):
        vendedor = params['username']
        fecha = params['fecha']
        comisiones = []
        if not vendedor:
            raise Exception('No existe ningún vendedor con ese usuario')
        registros = get(('''SELECT COUNT(id) FROM comisiones WHERE vendedor = %s and TO_CHAR(fecha,
        'DD/MM/YYYY') = %s'''), (vendedor, fecha), False)[0]
        if not registros:
            raise Exception('El usuario no tiene comisiones registradas en la fecha proporcionada')
        for i in range(registros):
            id, monto, pagado, fecha, pagado, pagado_en = get('''SELECT id, monto, pagado, fecha, pagado, pagado_en 
            FROM comisiones WHERE vendedor = %s and TO_CHAR(fecha,'DD/MM/YYYY') = %s''', (vendedor, fecha), False)
            if pagado_en:
                pagado_en.strftime("%d/%m/%Y")
            comisiones.append({'id': id, 'monto': monto, 'fecha': fecha.strftime("%d/%m/%Y"),'pagado': pagado, 'pagado_en': pagado_en})
        return comisiones

    @classmethod
    def buscar_comisiones(cls, params):
        vendedor = params['username']
        comisiones = []
        if not vendedor:
            raise Exception('No existe ningún vendedor con ese usuario')
        registros = get('''SELECT COUNT(id) FROM comisiones WHERE vendedor = %s''', (vendedor,), False)[0]
        if not registros:
            raise Exception('No hay comisiones registradas para este usuario')
        for i in range(registros):
            id, monto, pagado, fecha, pagado, pagado_en = get('''SELECT id, monto, pagado, fecha, pagado, pagado_en 
            FROM comisiones WHERE vendedor = %s''', (vendedor,), False)
            if pagado_en:
                pagado_en.strftime("%d/%m/%Y")
            comisiones.append({'id': id, 'monto': monto, 'fecha': fecha.strftime("%d/%m/%Y"), 'pagado': pagado, 'pagado_en': pagado_en})
        return comisiones

    @classmethod
    def registros_dia(cls, params):
        registros = get('''SELECT * FROM comisiones WHERE TO_CHAR(fecha, 'DD/MM/YYYY') = %s''', (params['fecha'],), True)
        if not registros:
            raise Exception('No hay ventas registradas para la fecha seleccionada')
        comisiones = []
        for i in range(len(registros)):
            comisiones.append(
                {'id': registros[i][0], 'vendedor': registros[i][1], 'monto': registros[i][2],
                 'pagado': registros[i][3], 'fecha': registros[i][4].strftime("%d/%m/%Y"), 'pagado_en': registros[i][5]})
        return comisiones


    @classmethod
    def comision_usuario_hoy(cls, params):
        hoy = datetime.datetime.now()
        hoy = hoy.strftime("%d/%m/%Y")
        exist = get('''SELECT id FROM usuario WHERE username = %s''',(params['username'],),False)
        if not exist:
            raise Exception('El usuario no existe')
        comision = get('''SELECT monto FROM comisiones WHERE vendedor = %s AND TO_CHAR(fecha,
                      'DD/MM/YYYY') = %s''', (params['username'], hoy), False)
        if not comision:
            return {'monto': 0}
        else:
            return {'monto': comision[0]}

    @classmethod
    def pagar_comision(cls, params):
        exist = get('''SELECT pagado_en FROM comisiones WHERE id = %s''',(params['id'],),False)
        if not exist:
            raise Exception('El no hay comisiones con el id proporcionado')
        if exist[0]:
            raise Exception(f'La comisión ya había sido pagada el día {exist[0].strftime("%d/%m/%Y")}')
        post('''UPDATE comisiones SET pagado = true, pagado_en = NOW()''',(),False)
        return  f'Comisión pagada exitosamente'