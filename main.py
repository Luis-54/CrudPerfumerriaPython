from database import conectar_db, inicializar_db
from models import Cliente, Perfume, Factura, DetalleFactura
from services import FacturacionService
from views import FacturacionService
import tkinter as tk
from views import FacturacionView
from database import conectar_db, inicializar_db
from services import FacturacionService

def main():
    db = conectar_db()
    inicializar_db(db)

    facturacion_service = FacturacionService(db)  # Instancia del servicio
    facturacion_view = FacturacionView(facturacion_service)  # Pasar el servicio a la vista

    # Crear la ventana principal
    root = tk.Tk()
    root.title("Sistema de Facturación de Perfumes")
    root.geometry("400x300")

    # Botones del menú principal
    btn_agregar_cliente = tk.Button(root, text="Agregar Cliente", command=facturacion_view.mostrar_agregar_cliente)
    btn_agregar_cliente.pack(pady=10)

    btn_agregar_perfume = tk.Button(root, text="Agregar Perfume", command=facturacion_view.mostrar_agregar_perfume)
    btn_agregar_perfume.pack(pady=10)

    btn_crear_factura = tk.Button(root, text="Crear Factura", command=facturacion_view.mostrar_crear_factura)
    btn_crear_factura.pack(pady=10)

    btn_ver_factura = tk.Button(root, text="Ver Factura", command=facturacion_view.mostrar_ver_factura)
    btn_ver_factura.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()