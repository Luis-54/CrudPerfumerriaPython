from models import Cliente, Perfume, Factura, DetalleFactura
from sqlite3 import Connection

class FacturacionService:
    def __init__(self, db: Connection):
        self.db = db

    def agregar_cliente(self, cliente: Cliente):
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT INTO Clientes (nombre, telefono, habitual)
            VALUES (?, ?, ?)
        ''', (cliente.nombre, cliente.telefono, cliente.habitual))
        self.db.commit()
        print("Cliente agregado correctamente.")

    def agregar_perfume(self, perfume: Perfume):
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                INSERT INTO Perfumes (nombre, precio)
                VALUES (?, ?)
            ''', (perfume.nombre, perfume.precio))
            self.db.commit()
            print("Perfume agregado correctamente.")
        except Exception as e:
            print(f"Error al agregar perfume: {e}")

    def crear_factura(self, factura: Factura, detalles: list[DetalleFactura]):
        cursor = self.db.cursor()
        # Insertar la factura
        cursor.execute('''
            INSERT INTO Facturas (cliente_id, total)
            VALUES (?, ?)
        ''', (factura.cliente.id if factura.cliente else None, factura.total))
        factura_id = cursor.lastrowid

        # Insertar los detalles de la factura
        for detalle in detalles:
            cursor.execute('''
                INSERT INTO DetallesFactura (factura_id, perfume_id, cantidad, precio)
                VALUES (?, ?, ?, ?)
            ''', (factura_id, detalle.perfume_id, detalle.cantidad, detalle.precio))

        self.db.commit()
        print("Factura creada correctamente.")

    def obtener_factura(self, factura_id: int):
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT * FROM Facturas WHERE id = ?
        ''', (factura_id,))
        factura = cursor.fetchone()
        if factura:
            return Factura(cliente=None, total=factura[2])  # Ajusta según tu modelo
        return None
    
    def obtener_todas_las_facturas(self):
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT Facturas.id, Clientes.nombre, Facturas.total
            FROM Facturas
            LEFT JOIN Clientes ON Facturas.cliente_id = Clientes.id
        ''')
        facturas = cursor.fetchall()
        return [
            {
                "id": factura[0],
                "cliente": factura[1] if factura[1] else "Cliente no especificado",
                "total": factura[2]
            }
            for factura in facturas
        ]