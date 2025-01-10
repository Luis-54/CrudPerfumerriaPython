from database import conectar_db, inicializar_db
from models import Cliente, Perfume, Factura, DetalleFactura
from services import FacturacionService
from views import FacturacionService
import tkinter as tk
from views import FacturacionView


def main():
    # Conectar a la base de datos e inicializarla
    db = conectar_db()
    inicializar_db(db)
    # Crear instancias del servicio y la vista
    facturacion_service = FacturacionService(db)
    facturacion_view = FacturacionView(facturacion_service)

    # Crear la ventana principal
    root = tk.Tk()
    root.title("Sistema de Facturación de Perfumes")
    root.geometry("400x300")

    # Botones del menú principal
    btn_agregar_cliente = tk.Button(root, text="Agregar Cliente", command=facturacion_view.mostrar_agregar_cliente)
    btn_agregar_cliente.pack(pady=10)

    btn_clientes_fidelizados = tk.Button(root, text="Clientes", command=facturacion_view.mostrar_todos_los_clientes)
    btn_clientes_fidelizados.pack(pady=10)

    btn_agregar_perfume = tk.Button(root, text="Agregar Perfume", command=facturacion_view.mostrar_agregar_perfume)
    btn_agregar_perfume.pack(pady=10)

    btn_crear_factura = tk.Button(root, text="Crear Factura", command=facturacion_view.mostrar_crear_factura)
    btn_crear_factura.pack(pady=10)

    btn_ver_factura = tk.Button(root, text="Ver Facturas", command=facturacion_view.mostrar_ver_factura)
    btn_ver_factura.pack(pady=10)

    # Iniciar el bucle principal de la aplicación
    root.mainloop()

if __name__ == "__main__":
    main()