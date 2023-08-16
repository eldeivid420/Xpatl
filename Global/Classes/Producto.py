"""
    Clase que describe un producto
    Authors: David Rodriguez Fragoso
    Created: 11/08/2023
    Last update: 14/08/2023
"""

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

        """
        Método que registra o sobreescribe un producto en la base de datos

        Parameters:
        * nombre: el nombre del producto
        * precio: el precio normal del producto
        * precio_esp: el precio especial del producto
        * disponibles: cantidad de productos disponibles
        * sku: el sku del producto

        Returns:

        """

        self.sku = params['sku']
        exist = self.exist()

        if exist:
            self.actualizar_producto(params)
            post('''UPDATE producto SET estatus = True WHERE sku = %s''', (self.sku,), False)
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

        """
        Método que carga un producto desde la base de datos

        Parameters:
        * sku: el sku del producto

        Returns:

        Un JSON con la información del producto
        """

        self.sku = params['sku']
        if self.exist():
            try:
                self.id, self.nombre, self.precio, self.precio_esp, self.disponibles, self.estatus = get(
                    '''SELECT id, nombre, precio, precio_esp, disponibles, estatus FROM producto WHERE sku = %s''',
                    (self.sku,), False
                )
            except Exception as e:
                return e, 400
        else:
            return f'El producto no existe', 400

    def exist(self):

        """
        Método que verifica si un producto existe

        Parameters:
        * sku: el sku del producto

        Returns:

        True si el producto existe
        """

        exist = get('''SELECT * FROM producto WHERE sku = %s''', (self.sku,))
        return exist

    def actualizar_producto(self, params):

        """
        Método que actualiza la información de un producto

        Parameters:
        * sku: el sku del producto

        Returns:

        Un string que confirma o rechaza la operación
        """

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

        """
        Método de clase que cambia el estatus de un producto a False

        Parameters:
        * sku: el sku del producto

        Returns:

        Un string que confirma la operación

        """

        sku = params['sku']
        post('''UPDATE producto SET estatus = False WHERE sku = %s''', (sku,), False)
        return f'Producto eliminado exitosamente'

    @classmethod
    def obtener_productos(cls):

        """
        Método de clase que obtiene todos los productos en la base de datos

        Parameters:

        Returns:

        Un diccionario con los productos

        """

        productos = {}
        todos = get('''SELECT * FROM producto where estatus = True''', (), True)
        for i in range(len(todos)):
            productos[i] = todos[i]
        return productos

    @classmethod
    def filtrar_productos(cls, params):

        """
        Método de clase que obtiene todos los productos filtrados desde la base de datos

        Parameters:
        * orden: alfabetico o numerico
        * invertido: true o false
        Returns:

        Un diccionario con los productos ordenados

        """

        productos = {}

        if params['orden'] == 'alfabetico' and params['invertido'] == True:
            todos = get('''SELECT * FROM producto where estatus = True ORDER BY nombre desc''', (), True)

        elif params['orden'] == 'precio' and params['invertido'] == True:
            todos = get('''SELECT * FROM producto where estatus = True ORDER BY precio desc''', (), True)

        elif params['orden'] == 'alfabetico':
            todos = get('''SELECT * FROM producto where estatus = True ORDER BY nombre''', (), True)

        elif params['orden'] == 'precio':
            todos = get('''SELECT * FROM producto where estatus = True ORDER BY precio''', (), True)

        for i in range(len(todos)):
            productos[i] = todos[i]

        return productos






