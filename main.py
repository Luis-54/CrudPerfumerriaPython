from database import conectar_db, inicializar_db
from models import Cliente, Perfume, Factura, DetalleFactura
from services import FacturacionService
from views import FacturacionView
import tkinter as tk
from tkinter import ttk

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
    root.geometry("500x600")
    root.resizable(False, False)  # Fijar tamaño de la ventana

    # Aplicar estilo
    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10)
    style.configure("TLabel", font=("Helvetica", 14), padding=5)
    style.configure("TFrame", background="#f2f2f2")

    # Crear un marco principal con fondo y bordes
    main_frame = ttk.Frame(root, padding=20, style="TFrame")
    main_frame.pack(fill="both", expand=True)

    # Título del sistema
    lbl_titulo = ttk.Label(main_frame, text="Sistema de Facturación de Perfumex", font=("Helvetica", 16, "bold"), anchor="center")
    lbl_titulo.pack(pady=20)

    # Botones del menú principal
    btn_agregar_cliente = ttk.Button(main_frame, text="Agregar Cliente", command=facturacion_view.mostrar_agregar_cliente)
    btn_agregar_cliente.pack(pady=10, fill="x")

    btn_clientes_fidelizados = ttk.Button(main_frame, text="Ver Clientes", command=facturacion_view.mostrar_todos_los_clientes)
    btn_clientes_fidelizados.pack(pady=10, fill="x")

    btn_agregar_perfume = ttk.Button(main_frame, text="Agregar Perfume", command=facturacion_view.mostrar_agregar_perfume)
    btn_agregar_perfume.pack(pady=10, fill="x")

    btn_perfumes = ttk.Button(main_frame, text="Ver Perfumes", command=facturacion_view.mostrar_todos_los_perfumes)
    btn_perfumes.pack(pady=10, fill="x")

    btn_crear_factura = ttk.Button(main_frame, text="Crear Factura", command=facturacion_view.mostrar_crear_factura)
    btn_crear_factura.pack(pady=10, fill="x")

    btn_factura = ttk.Button(main_frame, text="Ver Facturas", command=facturacion_view.mostrar_ver_facturas)
    btn_factura.pack(pady=10, fill="x")

    # Pie de página
    lbl_footer = ttk.Label(main_frame, text="© 2025 Facturación Perfumes. Todos los derechos reservados.", font=("Helvetica", 10), anchor="center")
    lbl_footer.pack(side="bottom", pady=20)

    # Iniciar el bucle principal de la aplicación
    root.mainloop()

if __name__ == "__main__":
    main()