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

    def obtener_todos_los_clientes(self):
        cursor = self.db.cursor()
        cursor.execute('''
        SELECT id, nombre, telefono, habitual
        FROM Clientes
        ''')
        clientes = cursor.fetchall()

        # Depuración: imprime los datos crudos obtenidos de la base de datos
        print("Datos crudos obtenidos de la base de datos:", clientes)

        # Procesar los datos
        return [
        {
            "id": cliente[0],
            "nombre": cliente[1] if cliente[1] else "Sin nombre",
            "telefono": cliente[2] if cliente[2] else "Sin teléfono",
            "habitual": "Sí" if cliente[3] == 1 else "No"
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

    def editar_cliente(self, cliente_id: int, nombre: str, telefono: str, habitual: bool):
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
                "habitual": "Sí" if cliente[3] else "No"
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

    def obtener_todos_los_clientes(self):
        cursor = self.db.cursor()
        cursor.execute('''
        SELECT id, nombre, telefono, habitual
        FROM Clientes
    ''')
        clientes = cursor.fetchall()

        # Depuración: imprime los datos crudos obtenidos de la base de datos
        print("Datos crudos obtenidos de la base de datos:", clientes)

        # Procesar los datos
        return [
        {
            "id": cliente[0],
            "nombre": cliente[1] if cliente[1] else "Sin nombre",
            "telefono": cliente[2] if cliente[2] else "Sin teléfono",
            "habitual": "Sí" if cliente[3] == 1 else "No"
        }
        for cliente in clientes
    ]


    def editar_perfume(self, perfume_id: int, nombre: str, precio: float, stock: int):
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                UPDATE Perfumes
                SET nombre = ?, precio = ?, stock = ?
                WHERE id = ?
        ''', (nombre, precio, stock, perfume_id))
            self.db.commit()
            print(f"Perfume con ID {perfume_id} editado correctamente.")
        except Exception as e:
            print(f"Error al editar perfume: {e}")


    def obtener_perfume_por_id(self, perfume_id: int):
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT id, nombre, precio, stock
            FROM Perfumes
            WHERE id = ?
        ''', (perfume_id,))
        perfume = cursor.fetchone()
        if perfume:
            return {
                "id": perfume[0],
                "nombre": perfume[1],
                "precio": perfume[2],
                "stock": perfume[3]
            }
        return None

    def eliminar_perfume(self, perfume_id: int):
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                DELETE FROM Perfumes
                WHERE id = ?
            ''', (perfume_id,))
            self.db.commit()
            print(f"Perfume con ID {perfume_id} eliminado correctamente.")
        except Exception as e:
            print(f"Error al eliminar perfume: {e}")

    def crear_factura(self, cliente_id, fecha, total, detalles):
        try:
            # Insertar la factura principal
            cursor = self.db.cursor()
            cursor.execute("""
                INSERT INTO Facturas (cliente_id, fecha, total)
                VALUES (?, ?, ?)
            """, (cliente_id, fecha, total))
            
            # Obtener el ID de la factura recién creada
            factura_id = cursor.lastrowid
            
            # Insertar los detalles de la factura
            for detalle in detalles:
                cursor.execute("""
                    INSERT INTO DetallesFactura (factura_id, perfume_id, cantidad, precio)
                    VALUES (?, ?, ?, ?)
                """, (factura_id, detalle['perfume_id'], detalle['cantidad'], detalle['precio_unitario']))
            
            self.db.commit()
            return factura_id
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al crear la factura: {str(e)}")

    def obtener_todos_los_clientes(self):
        cursor = self.db.cursor()
        cursor.execute('''
        SELECT id, nombre, telefono, habitual
        FROM Clientes
    ''')
        clientes = cursor.fetchall()

    # Depuración: imprime los datos crudos obtenidos de la base de datos
        print("Datos crudos obtenidos de la base de datos:", clientes)

    # Procesar los datos
        return [
        {
            "id": cliente[0],
            "nombre": cliente[1] if cliente[1] else "Sin nombre",
            "telefono": cliente[2] if cliente[2] else "Sin teléfono",
            "habitual": "Sí" if cliente[3] == 1 else "No"
        }
        for cliente in clientes
    ]


    def obtener_todos_los_perfumes(self):
        cursor = self.db.cursor()
        cursor.execute('''
        SELECT id, nombre, precio, stock
        FROM Perfumes
        ''')
        perfumes = cursor.fetchall()

    # Depuración: imprime los datos crudos obtenidos de la base de datos
        print("Datos crudos obtenidos de la base de datos de perfumes:", perfumes)

    # Procesar y devolver los datos
        return [
        {
            "id": perfume[0],
            "nombre": perfume[1] if perfume[1] else "Sin nombre",
            "precio": perfume[2] if perfume[2] is not None else 0.0,
            "stock": perfume[3] if perfume[3] is not None else 0
        }
        for perfume in perfumes
    ]

    def obtener_facturas(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT f.id, c.nombre, f.fecha, f.total 
                FROM Facturas f
                JOIN Clientes c ON f.cliente_id = c.id
                ORDER BY f.fecha DESC
            """)
            facturas = cursor.fetchall()
            
            return [{
                'id': f[0],
                'cliente_nombre': f[1],
                'fecha': f[2],
                'total': f[3]
            } for f in facturas]
        except Exception as e:
            raise Exception(f"Error al obtener facturas: {str(e)}")

    def obtener_detalles_factura(self, factura_id):
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT p.nombre, d.cantidad, d.precio, (d.cantidad * d.precio) as subtotal
                FROM DetallesFactura d
                JOIN Perfumes p ON d.perfume_id = p.id
                WHERE d.factura_id = ?
            """, (factura_id,))
            detalles = cursor.fetchall()
            
            return [{
                'perfume_nombre': d[0],
                'cantidad': d[1],
                'precio_unitario': d[2],
                'subtotal': d[3]
            } for d in detalles]
        except Exception as e:
            raise Exception(f"Error al obtener detalles: {str(e)}")
