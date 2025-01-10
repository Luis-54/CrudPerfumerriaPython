from tkinter import ttk
from services import FacturacionService
import tkinter as tk
from tkinter import messagebox
from models import Cliente, Perfume, Factura, DetalleFactura

class FacturacionView:
    def __init__(self, service):
        self.service = service

    import tkinter as tk
from tkinter import messagebox

class FacturacionView:
    def __init__(self, service):
        self.service = service

    def mostrar_agregar_cliente(self):
        # Ventana para agregar cliente
        ventana = tk.Toplevel()
        ventana.title("Agregar Cliente")

        # Campos del formulario
        tk.Label(ventana, text="Nombre:").grid(row=0, column=0, padx=10, pady=10)
        entry_nombre = tk.Entry(ventana)
        entry_nombre.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(ventana, text="Teléfono:").grid(row=1, column=0, padx=10, pady=10)
        entry_telefono = tk.Entry(ventana)
        entry_telefono.grid(row=1, column=1, padx=10, pady=10)

        # Checkbutton para marcar si el cliente es fidelizado
        habitual_var = tk.BooleanVar()
        chk_habitual = tk.Checkbutton(ventana, text="Cliente Fidelizado", variable=habitual_var)
        chk_habitual.grid(row=2, columnspan=2, pady=10)

        def agregar_cliente():
            nombre = entry_nombre.get()
            telefono = entry_telefono.get()
            habitual = habitual_var.get()  # Obtener el valor del Checkbutton

            if nombre and telefono:
                cliente = Cliente(nombre, telefono, habitual)
                self.service.agregar_cliente(cliente)
                messagebox.showinfo("Éxito", "Cliente agregado correctamente.")
                ventana.destroy()
            else:
                messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")

        btn_agregar = tk.Button(ventana, text="Agregar", command=agregar_cliente)
        btn_agregar.grid(row=3, columnspan=2, pady=10)
    
    def mostrar_todos_los_clientes(self):
        # Crear una ventana para mostrar todos los clientes
        ventana = tk.Toplevel()
        ventana.title("Todos los Clientes")

        # Crear un Treeview para mostrar los clientes en una tabla
        tree = ttk.Treeview(ventana, columns=("ID", "Nombre", "Teléfono", "Habitual"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Teléfono", text="Teléfono")
        tree.heading("Habitual", text="Habitual")
        tree.pack(fill="both", expand=True)

        # Función para actualizar la tabla
        def actualizar_tabla():
            # Limpiar la tabla actual
            for item in tree.get_children():
                tree.delete(item)

            # Obtener todos los clientes del servicio
            clientes = self.service.obtener_todos_los_clientes()

            # Agregar los clientes al Treeview
            for cliente in clientes:
                tree.insert("", "end", values=(cliente["id"], cliente["nombre"], cliente["telefono"], cliente["habitual"]))

        # Llamar a la función para cargar los datos iniciales
        actualizar_tabla()

        # Botón para eliminar cliente
        def eliminar_cliente():
            seleccionado = tree.selection()  # Obtener el cliente seleccionado
            if seleccionado:
                cliente_id = tree.item(seleccionado, "values")[0]  # Obtener el ID del cliente
                self.service.eliminar_cliente(cliente_id)  # Llamar al servicio para eliminar
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
                actualizar_tabla()  # Actualizar la tabla después de eliminar
            else:
                messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar.")

        btn_eliminar = tk.Button(ventana, text="Eliminar Cliente", command=eliminar_cliente)
        btn_eliminar.pack(pady=10)

        # Botón para editar cliente
        def editar_cliente():
            seleccionado = tree.selection()  # Obtener el cliente seleccionado
            if seleccionado:
                cliente_id = tree.item(seleccionado, "values")[0]  # Obtener el ID del cliente
                self.mostrar_editar_cliente(cliente_id, actualizar_tabla)  # Pasar la función de actualización
            else:
                messagebox.showwarning("Advertencia", "Seleccione un cliente para editar.")

        btn_editar = tk.Button(ventana, text="Editar Cliente", command=editar_cliente)
        btn_editar.pack(pady=10)

    def mostrar_editar_cliente(self, cliente_id: int, actualizar_tabla):
        # Obtener los datos del cliente desde el servicio
        cliente = self.service.obtener_cliente_por_id(cliente_id)

        # Crear una ventana para editar el cliente
        ventana_editar = tk.Toplevel()
        ventana_editar.title("Editar Cliente")

        # Campos para editar
        tk.Label(ventana_editar, text="Nombre:").grid(row=0, column=0)
        entry_nombre = tk.Entry(ventana_editar)
        entry_nombre.grid(row=0, column=1)
        entry_nombre.insert(0, cliente["nombre"])

        tk.Label(ventana_editar, text="Teléfono:").grid(row=1, column=0)
        entry_telefono = tk.Entry(ventana_editar)
        entry_telefono.grid(row=1, column=1)
        entry_telefono.insert(0, cliente["telefono"])

        tk.Label(ventana_editar, text="Habitual:").grid(row=2, column=0)
        entry_habitual = tk.Entry(ventana_editar)
        entry_habitual.grid(row=2, column=1)
        entry_habitual.insert(0, "Sí" if cliente["habitual"] == "Sí" else "No")

        # Función para guardar los cambios
        def guardar_cambios():
            nuevo_nombre = entry_nombre.get()
            nuevo_telefono = entry_telefono.get()
            nuevo_habitual = entry_habitual.get() == "Sí"
            self.service.editar_cliente(cliente_id, nuevo_nombre, nuevo_telefono, nuevo_habitual)
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")
            actualizar_tabla()  # Actualizar la tabla después de editar
            ventana_editar.destroy()  # Cerrar la ventana de edición

        btn_guardar = tk.Button(ventana_editar, text="Guardar Cambios", command=guardar_cambios)
        btn_guardar.grid(row=3, columnspan=2, pady=10)
    
    # Método para mostrar la ventana de agregar perfume
    def mostrar_agregar_perfume(self):  # Asegúrate de que esté dentro de la clase
        # Ventana para agregar perfume
        ventana = tk.Toplevel()
        ventana.title("Agregar Perfume")

        # Campos del formulario
        tk.Label(ventana, text="Nombre:").grid(row=0, column=0, padx=10, pady=10)
        entry_nombre = tk.Entry(ventana)
        entry_nombre.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(ventana, text="Precio:").grid(row=1, column=0, padx=10, pady=10)
        entry_precio = tk.Entry(ventana)
        entry_precio.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(ventana, text="Stock:").grid(row=2, column=0, padx=10, pady=10)
        entry_stock = tk.Entry(ventana)
        entry_stock.grid(row=2, column=1, padx=10, pady=10)

        # Función para agregar el perfume
        def agregar_perfume():
            nombre = entry_nombre.get()
            try:
                precio = float(entry_precio.get())
                stock = int(entry_stock.get())
                if nombre and precio > 0 and stock >= 0:
                    perfume = Perfume(nombre, precio, stock)
                    self.service.agregar_perfume(perfume)
                    messagebox.showinfo("Éxito", "Perfume agregado correctamente.")
                    ventana.destroy()
                else:
                    messagebox.showwarning("Advertencia", "Por favor, complete todos los campos correctamente.")
            except ValueError:
                messagebox.showwarning("Advertencia", "El precio y el stock deben ser números válidos.")

        btn_agregar = tk.Button(ventana, text="Agregar", command=agregar_perfume)
        btn_agregar.grid(row=3, columnspan=2, pady=10)

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