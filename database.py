import sqlite3

def conectar_db():
    return sqlite3.connect('facturacion.db')

def inicializar_db(db: sqlite3.Connection):
    # Crear tablas si no existen
    db.execute('''
        CREATE TABLE IF NOT EXISTS Clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            telefono TEXT,
            habitual INTEGER  -- Usar INTEGER para booleanos (0 = No, 1 = Sí)
        )
    ''')

    db.execute('''
        CREATE TABLE IF NOT EXISTS Perfumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            precio REAL,
            stock INTEGER  -- Nueva columna para el stock
        )
    ''')

    # Crear tabla principal de Facturas
    db.execute('''
        CREATE TABLE IF NOT EXISTS Facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            total REAL NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY(cliente_id) REFERENCES Clientes(id)
        )
    ''')

    # Crear tabla de detalles de factura (usar DetallesFactura en plural)
    db.execute('''
        CREATE TABLE IF NOT EXISTS DetallesFactura (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            factura_id INTEGER,
            perfume_id INTEGER,
            cantidad INTEGER,
            precio REAL,
            FOREIGN KEY(factura_id) REFERENCES Facturas(id),
            FOREIGN KEY(perfume_id) REFERENCES Perfumes(id)
        )
    ''')
    db.commit()