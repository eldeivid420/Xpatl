from Global.Utils.db import post, get


class Producto:

    def __init__(self, params, load=True):
        self.id = None
        self.nombre = None
        self.precio = None
        self.precio_esp = None
        self.disponibles = None
        self.sku = None
        self.load(params) if load else self.create(params)

    def create(self, params):

        self.sku = params['sku']
        exist = get('''SELECT * FROM producto WHERE sku = %s''', (self.sku,))

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
            self.nombre, self.precio, self.precio_esp, self.disponibles = get(
                '''SELECT id, nombre, precio, precio_esp, disponibles FROM producto WHERE sku = %s''',
                (self.sku,), False
            )
        except Exception as e:
            return e, 400

    def actualizar_producto(self, params):
        self.nombre = params['nombre']
        self.precio = params['precio']
        self.precio_esp = params['precio_esp']
        self.disponibles = params['disponibles']
        post('''UPDATE producto SET nombre = %s, precio = %s, precio_esp = %s, disponibles = %s WHERE sku = %s''',
             (self.nombre, self.precio, self.precio_esp, self.disponibles, self.sku), False)

    @classmethod
    def obtener_productos(cls):
        # Buscar forma de obtener todos sin usar el ID
        productos = {}
        registros = get('''SELECT COUNT(id) FROM producto''', (), False)[0]
        todos = get('''SELECT * FROM producto''', (), True)
        for i in range(len(todos)):
            productos[i] = todos[i]
        return productos




