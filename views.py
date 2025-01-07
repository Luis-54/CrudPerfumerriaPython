from tkinter import ttk
from services import FacturacionService
import tkinter as tk
from tkinter import messagebox
from models import Cliente, Perfume, Factura, DetalleFactura

class FacturacionView:
    def __init__(self, service):
        self.service = service

    def mostrar_agregar_cliente(self):
        # Ventana para agregar cliente
        ventana = tk.Toplevel()
        ventana.title("Agregar Cliente")

        tk.Label(ventana, text="Nombre:").grid(row=0, column=0, padx=10, pady=10)
        entry_nombre = tk.Entry(ventana)
        entry_nombre.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(ventana, text="Teléfono:").grid(row=1, column=0, padx=10, pady=10)
        entry_telefono = tk.Entry(ventana)
        entry_telefono.grid(row=1, column=1, padx=10, pady=10)

        def agregar_cliente():
            nombre = entry_nombre.get()
            telefono = entry_telefono.get()
            if nombre and telefono:
                cliente = Cliente(nombre, telefono)
                self.service.agregar_cliente(cliente)
                messagebox.showinfo("Éxito", "Cliente agregado correctamente.")
                ventana.destroy()
            else:
                messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")

        btn_agregar = tk.Button(ventana, text="Agregar", command=agregar_cliente)
        btn_agregar.grid(row=2, columnspan=2, pady=10)

    class FacturacionView:
        def __init__(self, service):
            self.service = service

    def mostrar_agregar_perfume(self):
        # Ventana para agregar perfume
        ventana = tk.Toplevel()
        ventana.title("Agregar Perfume")

        tk.Label(ventana, text="Nombre:").grid(row=0, column=0, padx=10, pady=10)
        entry_nombre = tk.Entry(ventana)
        entry_nombre.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(ventana, text="Precio:").grid(row=1, column=0, padx=10, pady=10)
        entry_precio = tk.Entry(ventana)
        entry_precio.grid(row=1, column=1, padx=10, pady=10)

        def agregar_perfume():
            nombre = entry_nombre.get()
            try:
                precio = float(entry_precio.get())
                if nombre and precio > 0:
                    perfume = Perfume(nombre, precio)
                    self.service.agregar_perfume(perfume)
                    messagebox.showinfo("Éxito", "Perfume agregado correctamente.")
                    ventana.destroy()
                else:
                    messagebox.showwarning("Advertencia", "Por favor, complete todos los campos correctamente.")
            except ValueError:
                messagebox.showwarning("Advertencia", "El precio debe ser un número válido.")

        btn_agregar = tk.Button(ventana, text="Agregar", command=agregar_perfume)
        btn_agregar.grid(row=2, columnspan=2, pady=10)

    def mostrar_crear_factura(self):
        # Ventana para crear factura
        ventana = tk.Toplevel()
        ventana.title("Crear Factura")

        # Aquí puedes agregar campos para seleccionar cliente y perfumes, y un botón para crear la factura

    def mostrar_ver_factura(self):
        # Crear una ventana para mostrar las facturas
        ventana = tk.Toplevel()
        ventana.title("Ver Facturas")

        # Crear un Treeview para mostrar las facturas en una tabla
        tree = ttk.Treeview(ventana, columns=("ID", "Cliente", "Total"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Cliente", text="Cliente")
        tree.heading("Total", text="Total")
        tree.pack(fill="both", expand=True)

        # Obtener todas las facturas del servicio
        facturas = self.service.obtener_todas_las_facturas()

        # Agregar las facturas al Treeview
        for factura in facturas:
            tree.insert("", "end", values=(factura["id"], factura["cliente"], factura["total"]))