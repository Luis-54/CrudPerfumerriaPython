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
        # Ventana para ver factura
        ventana = tk.Toplevel()
        ventana.title("Ver Factura")

        # Aquí puedes agregar lógica para mostrar las facturas existentes

    def mostrar_eliminar_factura(self):
        # Ventana para eliminar factura
        ventana = tk.Toplevel()
        ventana.title("Eliminar Factura")

        tk.Label(ventana, text="ID de la factura:").grid(row=0, column=0, padx=10, pady=10)
        entry_id = tk.Entry(ventana)
        entry_id.grid(row=0, column=1, padx=10, pady=10)

        def eliminar_factura():
            try:
                factura_id = int(entry_id.get())
                self.service.eliminar_factura(factura_id)
                messagebox.showinfo("Éxito", "Factura eliminada correctamente.")
                ventana.destroy()
            except ValueError:
                messagebox.showwarning("Advertencia", "Por favor, ingrese un ID válido.")

        btn_eliminar = tk.Button(ventana, text="Eliminar", command=eliminar_factura)
        btn_eliminar.grid(row=1, columnspan=2, pady=10)