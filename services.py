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

    def obtener_todos_los_clientes(self):  # Cambia el nombre del método
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT id, nombre, telefono, habitual
            FROM Clientes
    ''')  # Sin condición WHERE
        clientes = cursor.fetchall()
        return [
        {
            "id": cliente[0],
            "nombre": cliente[1],
            "telefono": cliente[2],
            "habitual": "Sí" if cliente[3] else "No"  # Convertir a texto
        }
        for cliente in clientes
    ]

    def eliminar_cliente(self, cliente_id: int):
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                DELETE FROM Clientes
                WHERE id = ?
            ''', (cliente_id,))
            self.db.commit()
            print(f"Cliente con ID {cliente_id} eliminado correctamente.")
        except Exception as e:
            print(f"Error al eliminar cliente: {e}")

    def editar_cliente(self, cliente_id: int, nombre: str, telefono: str, habitual: bool):  # Asegúrate de que esté dentro de la clase
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                UPDATE Clientes
                SET nombre = ?, telefono = ?, habitual = ?
                WHERE id = ?
            ''', (nombre, telefono, habitual, cliente_id))
            self.db.commit()
            print(f"Cliente con ID {cliente_id} editado correctamente.")
        except Exception as e:
            print(f"Error al editar cliente: {e}")

    def obtener_cliente_por_id(self, cliente_id: int):
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT id, nombre, telefono, habitual
            FROM Clientes
            WHERE id = ?
        ''', (cliente_id,))
        cliente = cursor.fetchone()
        if cliente:
            return {
                "id": cliente[0],
                "nombre": cliente[1],
                "telefono": cliente[2],
                "habitual": "Sí" if cliente[3] else "No"  # Convertir a texto
            }
        return None

    def editar_cliente(self, cliente_id: int, nombre: str, telefono: str, habitual: str):  # Asegúrate de que esté dentro de la clase
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                UPDATE Clientes
                SET nombre = ?, telefono = ?, habitual = ?
                WHERE id = ?
            ''', (nombre, telefono, habitual, cliente_id))
            self.db.commit()
            print(f"Cliente con ID {cliente_id} editado correctamente.")
        except Exception as e:
            print(f"Error al editar cliente: {e}")

    def agregar_perfume(self, perfume: Perfume):  # Asegúrate de que esté dentro de la clase
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                INSERT INTO Perfumes (nombre, precio, stock)
                VALUES (?, ?, ?)
            ''', (perfume.nombre, perfume.precio, perfume.stock))
            self.db.commit()
            print("Perfume agregado correctamente.")
        except Exception as e:
            print(f"Error al agregar perfume: {e}")

    def obtener_todos_los_perfumes(self):
        cursor = self.db.cursor()
        cursor.execute('''
        SELECT id, nombre, precio, stock
        FROM Perfumes
    ''')  # Sin condición WHERE
        perfumes = cursor.fetchall()
        print("Perfumes obtenidos de la base de datos:", perfumes)  # Depuración
        return [
        {
            "id": perfume[0],
            "nombre": perfume[1],
            "precio": perfume[2],
            "stock": perfume[3]
        }
        for perfume in perfumes
    ]

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