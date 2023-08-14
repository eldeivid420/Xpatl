from Global.Utils.db import post, get


class Producto:

    def __init__(self, params, load=True):
        self.id = None
        self.nombre = None
        self.precio = None
        self.precio_esp = None
        self.disponibles = None
        self.sku = None
        self.estatus = None
        self.load(params) if load else self.create(params)

    def create(self, params):

        self.sku = params['sku']
        exist = self.exist()

        if exist:
            self.actualizar_producto(params)
            return 'Producto actualizado correctamente'
        else:
            try:
                self.nombre = params['nombre']
                self.precio = params['precio']
                self.precio_esp = params['precio_esp'],
                self.disponibles = params['disponibles']
                self.id = post(
                    '''INSERT INTO producto (nombre, precio, precio_esp, disponibles, sku) VALUES (%s,%s,%s,%s,
                    %s) RETURNING id''',
                    (self.nombre, self.precio, self.precio_esp, self.disponibles, self.sku), True)[0]
            except Exception as e:
                return str(e), 400

    def load(self, params):
        self.sku = params['sku']
        try:
            self.id, self.nombre, self.precio, self.precio_esp, self.disponibles, self.estatus = get(
                '''SELECT id, nombre, precio, precio_esp, disponibles, estatus FROM producto WHERE sku = %s''',
                (self.sku,), False
            )
        except Exception as e:
            return e, 400

    def exist(self):
        exist = get('''SELECT * FROM producto WHERE sku = %s''', (self.sku,))
        return exist

    def actualizar_producto(self, params):
        exist = self.exist()
        if exist:
            self.nombre = params['nombre']
            self.precio = params['precio']
            self.precio_esp = params['precio_esp']
            self.disponibles = params['disponibles']
            post('''UPDATE producto SET nombre = %s, precio = %s, precio_esp = %s, disponibles = %s WHERE sku = %s''',
                 (self.nombre, self.precio, self.precio_esp, self.disponibles, self.sku), False)
            return f'Producto actualizado correctamente'
        else:
            return f'No existe el producto'

    @classmethod
    def eliminar_producto(cls, params):
        sku = params['sku']
        post('''UPDATE producto SET estatus = False WHERE sku = %s''', (sku,), False)
        return f'Producto eliminado exitosamente'

    @classmethod
    def obtener_productos(cls):
        productos = {}
        todos = get('''SELECT * FROM producto''', (), True)
        for i in range(len(todos)):
            productos[i] = todos[i]
        return productos




