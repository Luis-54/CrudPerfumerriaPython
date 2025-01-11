from sqlite3 import Connection

class Cliente:
    def __init__(self, nombre: str = None, telefono: str = None, habitual: bool = False):
        self.nombre = nombre
        self.telefono = telefono
        self.habitual = habitual

class Perfume:
    def __init__(self, nombre: str, precio: float, stock: int = 0):  # Agregar stock
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

class Factura:
    def __init__(self, cliente: Cliente = None, total: float = 0, fecha: str = None):
        self.cliente = cliente
        self.total = total
        self.fecha = fecha

class DetalleFactura:
    def __init__(self, factura_id: int, perfume_id: int, cantidad: int, precio: float):
        self.factura_id = factura_id
        self.perfume_id = perfume_id
        self.cantidad = cantidad
        self.precio = precio
