import datetime
import sqlite3
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
        ventana.geometry("400x300")
        ventana.resizable(False, False)

        frame = ttk.Frame(ventana, padding="20")
        frame.pack(fill="both", expand=True)

        # Campos del formulario
        ttk.Label(frame, text="Nombre:", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        entry_nombre = ttk.Entry(frame, font=("Helvetica", 12))
        entry_nombre.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(frame, text="Teléfono:", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        entry_telefono = ttk.Entry(frame, font=("Helvetica", 12))
        entry_telefono.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        habitual_var = tk.BooleanVar()
        chk_habitual = ttk.Checkbutton(frame, text="Cliente Fidelizado", variable=habitual_var, style="TCheckbutton")
        chk_habitual.grid(row=2, columnspan=2, pady=10)

        frame.columnconfigure(1, weight=1)

        def agregar_cliente():
            nombre = entry_nombre.get()
            telefono = entry_telefono.get()
            habitual = habitual_var.get()

            if nombre and telefono:
                cliente = Cliente(nombre, telefono, habitual)
                try:
                    self.service.agregar_cliente(cliente)
                    messagebox.showinfo("Éxito", "Cliente agregado correctamente.")
                    ventana.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo agregar el cliente: {str(e)}")
            else:
                messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")

        btn_agregar = ttk.Button(frame, text="Agregar", command=agregar_cliente)
        btn_agregar.grid(row=3, columnspan=2, pady=20)

    
    def mostrar_todos_los_clientes(self):
        ventana = tk.Toplevel()
        ventana.title("Todos los Clientes")
        ventana.geometry("600x400")

        frame = ttk.Frame(ventana, padding="10")
        frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(frame, columns=("ID", "Nombre", "Teléfono", "Habitual"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Teléfono", text="Teléfono")
        tree.heading("Habitual", text="Habitual")
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        def actualizar_tabla():
            for item in tree.get_children():
                tree.delete(item)

            try:
                clientes = self.service.obtener_todos_los_clientes()
                for cliente in clientes:
                        tree.insert("", "end", values=(
                    cliente["id"],
                    cliente["nombre"],
                    cliente["telefono"],
                    cliente["habitual"]
                ))
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar clientes: {str(e)}")

        actualizar_tabla()

        def eliminar_cliente():
            seleccionado = tree.selection()
            if seleccionado:
                cliente_id = tree.item(seleccionado, "values")[0]
            try:
                self.service.eliminar_cliente(cliente_id)
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
                actualizar_tabla()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el cliente: {str(e)}")
            else:
                messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar.")

        btn_eliminar = ttk.Button(frame, text="Eliminar Cliente", command=eliminar_cliente)
        btn_eliminar.pack(side="left", padx=10, pady=10)

        def editar_cliente():
            seleccionado = tree.selection()
            if seleccionado:
                cliente_id = tree.item(seleccionado, "values")[0]
                self.mostrar_editar_cliente(cliente_id, actualizar_tabla)
            else:
                messagebox.showwarning("Advertencia", "Seleccione un cliente para editar.")

        btn_editar = ttk.Button(frame, text="Editar Cliente", command=editar_cliente)
        btn_editar.pack(side="left", padx=10, pady=10)

        btn_cerrar = ttk.Button(frame, text="Cerrar", command=ventana.destroy)
        btn_cerrar.pack(side="right", padx=10, pady=10)

    def mostrar_editar_cliente(self, cliente_id: int, actualizar_tabla):
        cliente = self.service.obtener_cliente_por_id(cliente_id)

        ventana_editar = tk.Toplevel()
        ventana_editar.title("Editar Cliente")
        ventana_editar.geometry("400x300")
        ventana_editar.resizable(False, False)

        frame = ttk.Frame(ventana_editar, padding="20")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Nombre:", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        entry_nombre = ttk.Entry(frame, font=("Helvetica", 12))
        entry_nombre.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        entry_nombre.insert(0, cliente["nombre"])

        ttk.Label(frame, text="Teléfono:", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        entry_telefono = ttk.Entry(frame, font=("Helvetica", 12))
        entry_telefono.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        entry_telefono.insert(0, cliente["telefono"])

        ttk.Label(frame, text="Habitual:", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        habitual_var = tk.BooleanVar(value=(cliente["habitual"] == "Sí"))
        chk_habitual = ttk.Checkbutton(frame, text="Cliente Fidelizado", variable=habitual_var)
        chk_habitual.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        frame.columnconfigure(1, weight=1)

        def guardar_cambios():
            nuevo_nombre = entry_nombre.get()
            nuevo_telefono = entry_telefono.get()
            nuevo_habitual = habitual_var.get()
            try:
                self.service.editar_cliente(cliente_id, nuevo_nombre, nuevo_telefono, nuevo_habitual)
                messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")
                actualizar_tabla()
                ventana_editar.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar el cliente: {str(e)}")

        btn_guardar = ttk.Button(frame, text="Guardar Cambios", command=guardar_cambios)
        btn_guardar.grid(row=3, columnspan=2, pady=20)


    def mostrar_agregar_perfume(self):
        ventana = tk.Toplevel()
        ventana.title("Agregar Perfume")
        ventana.geometry("400x300")
        ventana.resizable(False, False)

        frame = ttk.Frame(ventana, padding="20")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Nombre:", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        entry_nombre = ttk.Entry(frame, font=("Helvetica", 12))
        entry_nombre.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(frame, text="Precio:", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        entry_precio = ttk.Entry(frame, font=("Helvetica", 12))
        entry_precio.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(frame, text="Stock:", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        entry_stock = ttk.Entry(frame, font=("Helvetica", 12))
        entry_stock.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        frame.columnconfigure(1, weight=1)

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

        btn_agregar = ttk.Button(frame, text="Agregar", command=agregar_perfume)
        btn_agregar.grid(row=3, columnspan=2, pady=20)

    def mostrar_todos_los_perfumes(self):
        ventana = tk.Toplevel()
        ventana.title("Todos los Perfumes")
        ventana.geometry("600x400")

        frame = ttk.Frame(ventana, padding="10")
        frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(frame, columns=("ID", "Nombre", "Precio", "Stock"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Precio", text="Precio")
        tree.heading("Stock", text="Stock")
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        def actualizar_tabla():
            for item in tree.get_children():
                tree.delete(item)

            try:
                perfumes = self.service.obtener_todos_los_perfumes()
                for perfume in perfumes:
                    tree.insert("", "end", values=(
                        perfume["id"],
                        perfume["nombre"],
                        f"${perfume['precio']:.2f}" if perfume["precio"] is not None else "$0.00",
                        perfume["stock"] if perfume["stock"] is not None else 0
                    ))
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar perfumes: {str(e)}")

        actualizar_tabla()

        def eliminar_perfume():
            seleccionado = tree.selection()
            if seleccionado:
                perfume_id = tree.item(seleccionado, "values")[0]
                try:
                    self.service.eliminar_perfume(perfume_id)
                    messagebox.showinfo("Éxito", "Perfume eliminado correctamente.")
                    actualizar_tabla()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo eliminar el perfume: {str(e)}")
            else:
                messagebox.showwarning("Advertencia", "Seleccione un perfume para eliminar.")

        btn_eliminar = ttk.Button(frame, text="Eliminar Perfume", command=eliminar_perfume)
        btn_eliminar.pack(side="left", padx=10, pady=10)

        def editar_perfume():
            seleccionado = tree.selection()
            if seleccionado:
                perfume_id = tree.item(seleccionado, "values")[0]
                self.mostrar_editar_perfume(perfume_id)
            else:
                messagebox.showwarning("Advertencia", "Seleccione un perfume para editar.")

        btn_editar = ttk.Button(frame, text="Editar Perfume", command=editar_perfume)
        btn_editar.pack(side="left", padx=10, pady=10)

        btn_cerrar = ttk.Button(frame, text="Cerrar", command=ventana.destroy)
        btn_cerrar.pack(side="right", padx=10, pady=10)

    def mostrar_editar_perfume(self, perfume_id: int):
        perfume = self.service.obtener_perfume_por_id(perfume_id)

        ventana_editar = tk.Toplevel()
        ventana_editar.title("Editar Perfume")
        ventana_editar.geometry("400x300")
        ventana_editar.resizable(False, False)

        frame = ttk.Frame(ventana_editar, padding="20")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Nombre:", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        entry_nombre = ttk.Entry(frame, font=("Helvetica", 12))
        entry_nombre.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        entry_nombre.insert(0, perfume["nombre"])

        ttk.Label(frame, text="Precio:", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        entry_precio = ttk.Entry(frame, font=("Helvetica", 12))
        entry_precio.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        entry_precio.insert(0, perfume["precio"])

        ttk.Label(frame, text="Stock:", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        entry_stock = ttk.Entry(frame, font=("Helvetica", 12))
        entry_stock.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        entry_stock.insert(0, perfume["stock"] if perfume["stock"] is not None else 0)

        frame.columnconfigure(1, weight=1)

        def guardar_cambios():
            nuevo_nombre = entry_nombre.get()
            nuevo_precio = float(entry_precio.get())
            nuevo_stock = int(entry_stock.get())
            try:
                self.service.editar_perfume(perfume_id, nuevo_nombre, nuevo_precio, nuevo_stock)
                messagebox.showinfo("Éxito", "Perfume actualizado correctamente.")
                ventana_editar.destroy()
                self.mostrar_todos_los_perfumes()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar el perfume: {str(e)}")

        btn_guardar = ttk.Button(frame, text="Guardar Cambios", command=guardar_cambios)
        btn_guardar.grid(row=3, columnspan=2, pady=20)


    def mostrar_crear_factura(self):
        # Ventana para crear factura
        ventana = tk.Toplevel()
        ventana.title("Crear Factura")
        ventana.geometry("600x800")

        # Frame principal
        main_frame = ttk.Frame(ventana, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Inicializar el Treeview para los perfumes
        self.perfumes_listbox = ttk.Treeview(main_frame, 
            columns=('Perfume', 'Cantidad', 'Precio Unit.', 'Subtotal', 'ID'),
            show='headings', 
            height=6)

        # Configurar las columnas visibles
        for col in ('Perfume', 'Cantidad', 'Precio Unit.', 'Subtotal'):
            self.perfumes_listbox.heading(col, text=col)
            self.perfumes_listbox.column(col, width=100)

        # Ocultar la columna ID
        self.perfumes_listbox.column('ID', width=0, stretch=False)

        try:
            # Obtener datos usando el servicio
            clientes = self.service.obtener_todos_los_clientes()
            perfumes = self.service.obtener_todos_los_perfumes()
    
            # Crear diccionarios como variables de instancia
            self.cliente_dict = {cliente["nombre"]: cliente["id"] for cliente in clientes}
            self.precios_perfumes = {perfume["nombre"]: perfume["precio"] for perfume in perfumes}
            self.perfumes_dict = {perfume["nombre"]: int(perfume["id"]) for perfume in perfumes}

            # Fecha
            fecha_frame = ttk.Frame(main_frame)
            fecha_frame.pack(fill=tk.X, pady=5)
        
            fecha_label = ttk.Label(fecha_frame, text="Fecha:")
            fecha_label.pack(side=tk.LEFT)
        
            self.fecha_entry = ttk.Entry(fecha_frame)
            self.fecha_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            self.fecha_entry.insert(0, datetime.datetime.now().strftime('%Y-%m-%d'))

            # Cliente
            cliente_frame = ttk.Frame(main_frame)
            cliente_frame.pack(fill=tk.X, pady=5)
        
            cliente_label = ttk.Label(cliente_frame, text="Cliente:")
            cliente_label.pack(side=tk.LEFT)
        
            self.cliente_combo = ttk.Combobox(cliente_frame, values=list(self.cliente_dict.keys()))
            self.cliente_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

            # Frame para perfume y cantidad
            perfume_frame = ttk.LabelFrame(main_frame, text="Agregar Perfume")
            perfume_frame.pack(fill=tk.X, pady=10, padx=5)

            perfume_label = ttk.Label(perfume_frame, text="Perfume:")
            perfume_label.grid(row=0, column=0, padx=5, pady=5)
        
            self.perfume_combo = ttk.Combobox(perfume_frame, values=list(self.precios_perfumes.keys()))
            self.perfume_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

            cantidad_label = ttk.Label(perfume_frame, text="Cantidad:")
            cantidad_label.grid(row=0, column=2, padx=5, pady=5)
        
            self.cantidad_spinbox = ttk.Spinbox(perfume_frame, from_=1, to=100, width=5)
            self.cantidad_spinbox.grid(row=0, column=3, padx=5, pady=5)

            perfume_frame.grid_columnconfigure(1, weight=1)

            # Lista de perfumes seleccionados (reemplazar la definición anterior)
            self.perfumes_listbox = ttk.Treeview(main_frame, 
                columns=('Perfume', 'Cantidad', 'Precio Unit.', 'Subtotal', 'ID'),
                show='headings', 
                height=6)
            self.perfumes_listbox.pack(fill=tk.BOTH, expand=True, pady=10)

            # Configurar las columnas
            for col in ('Perfume', 'Cantidad', 'Precio Unit.', 'Subtotal'):
                self.perfumes_listbox.heading(col, text=col)
                self.perfumes_listbox.column(col, width=100)
            
            # Ocultar la columna ID
            self.perfumes_listbox.heading('ID', text='ID')
            self.perfumes_listbox.column('ID', width=0, stretch=False)

            # Total
            total_frame = ttk.Frame(main_frame)
            total_frame.pack(fill=tk.X, pady=5)
        
            total_label = ttk.Label(total_frame, text="Total:")
            total_label.pack(side=tk.LEFT)
        
            self.total_value = ttk.Label(total_frame, text="$0.00")
            self.total_value.pack(side=tk.LEFT, padx=5)

            # Botones
            btn_frame = ttk.Frame(main_frame)
            btn_frame.pack(fill=tk.X, pady=10)

            ttk.Button(btn_frame, text="Agregar Perfume", 
                      command=lambda: self.agregar_perfume_a_factura(ventana)).pack(side=tk.LEFT, padx=5)
        
            ttk.Button(btn_frame, text="Eliminar Perfume", 
                      command=lambda: self.eliminar_perfume_de_factura(ventana)).pack(side=tk.LEFT, padx=5)
        
            ttk.Button(btn_frame, text="Guardar", 
                      command=lambda: self.guardar_factura(ventana)).pack(side=tk.LEFT, padx=5)

        except Exception as e:
            messagebox.showerror("Error", f"Error al crear la factura: {str(e)}")
            ventana.destroy()

    def agregar_perfume_a_factura(self, ventana):
        perfume_seleccionado = self.perfume_combo.get()
        try:
            cantidad = int(self.cantidad_spinbox.get())
            if perfume_seleccionado and cantidad > 0:
                precio_unitario = self.precios_perfumes[perfume_seleccionado]
                subtotal = precio_unitario * cantidad
            
                # Agregar a la lista
                self.perfumes_listbox.insert('', 'end', values=(
                    perfume_seleccionado,
                    cantidad,
                    f"${precio_unitario:.2f}",
                    f"${subtotal:.2f}",
                    self.perfumes_dict[perfume_seleccionado]
                ))
            
                # Actualizar total
                total_actual = float(self.total_value.cget("text").replace("$", ""))
                nuevo_total = total_actual + subtotal
                self.total_value.config(text=f"${nuevo_total:.2f}")
            
                # Limpiar selección
                self.perfume_combo.set('')
                self.cantidad_spinbox.set('1')
            else:
                messagebox.showwarning("Advertencia", "Seleccione un perfume y cantidad válida")
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número válido")

    def eliminar_perfume_de_factura(self, ventana):
        seleccion = self.perfumes_listbox.selection()
        if seleccion:
            for item in seleccion:
                valores = self.perfumes_listbox.item(item)['values']
                subtotal = float(valores[3].replace("$", ""))
                # Actualizar total
                total_actual = float(self.total_value.cget("text").replace("$", ""))
                nuevo_total = total_actual - subtotal
                self.total_value.config(text=f"${nuevo_total:.2f}")
                self.perfumes_listbox.delete(item)
        else:
            messagebox.showwarning("Advertencia", "Seleccione un perfume para eliminar")

    def guardar_factura(self, ventana):
        try:
            # Verificar que haya un cliente seleccionado
            cliente_nombre = self.cliente_combo.get()
            if not cliente_nombre:
                messagebox.showwarning("Advertencia", "Por favor seleccione un cliente")
                return

            # Verificar que haya perfumes en la lista
            if not self.perfumes_listbox.get_children():
                messagebox.showwarning("Advertencia", "Agregue al menos un perfume a la factura")
                return

            # Obtener los datos de la factura
            total_factura = float(self.total_value.cget("text").replace("$", ""))
            cliente_id = self.cliente_dict[cliente_nombre]
            fecha = self.fecha_entry.get()

            # Preparar los detalles de la factura
            detalles = []
            for item_id in self.perfumes_listbox.get_children():
                item = self.perfumes_listbox.item(item_id)['values']
                detalle = {
                    'perfume_id': item[4],  # ID del perfume
                    'cantidad': item[1],
                    'precio_unitario': float(item[2].replace("$", "")),
                }
                detalles.append(detalle)

            # Guardar usando el servicio
            self.service.crear_factura(
                cliente_id=cliente_id,
                fecha=fecha,
                total=total_factura,
                detalles=detalles
            )
            
            messagebox.showinfo("Éxito", "Factura guardada correctamente")
            ventana.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar la factura: {str(e)}")


    def mostrar_ver_facturas(self):
        # Crear ventana
        ventana = tk.Toplevel()
        ventana.title("Ver Facturas")
        ventana.geometry("800x600")

        # Frame principal
        main_frame = ttk.Frame(ventana, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Lista de facturas
        facturas_frame = ttk.LabelFrame(main_frame, text="Facturas", padding="5")
        facturas_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Crear Treeview para las facturas
        self.facturas_tree = ttk.Treeview(facturas_frame, 
            columns=('ID', 'Cliente', 'Fecha', 'Total'),
            show='headings', 
            height=10)

        # Configurar columnas
        self.facturas_tree.heading('ID', text='# Factura')
        self.facturas_tree.heading('Cliente', text='Cliente')
        self.facturas_tree.heading('Fecha', text='Fecha')
        self.facturas_tree.heading('Total', text='Total')

        self.facturas_tree.column('ID', width=80)
        self.facturas_tree.column('Cliente', width=200)
        self.facturas_tree.column('Fecha', width=100)
        self.facturas_tree.column('Total', width=100)

        # Agregar scrollbar
        scrollbar = ttk.Scrollbar(facturas_frame, orient=tk.VERTICAL, command=self.facturas_tree.yview)
        self.facturas_tree.configure(yscrollcommand=scrollbar.set)

        # Empaquetar Treeview y scrollbar
        self.facturas_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Frame para detalles de la factura
        detalles_frame = ttk.LabelFrame(main_frame, text="Detalles de la Factura", padding="5")
        detalles_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Treeview para los detalles
        self.detalles_tree = ttk.Treeview(detalles_frame,
            columns=('Perfume', 'Cantidad', 'Precio Unit.', 'Subtotal'),
            show='headings',
            height=6)

        # Configurar columnas de detalles
        self.detalles_tree.heading('Perfume', text='Perfume')
        self.detalles_tree.heading('Cantidad', text='Cantidad')
        self.detalles_tree.heading('Precio Unit.', text='Precio Unitario')
        self.detalles_tree.heading('Subtotal', text='Subtotal')

        self.detalles_tree.column('Perfume', width=200)
        self.detalles_tree.column('Cantidad', width=100)
        self.detalles_tree.column('Precio Unit.', width=100)
        self.detalles_tree.column('Subtotal', width=100)

        # Scrollbar para detalles
        detalles_scrollbar = ttk.Scrollbar(detalles_frame, orient=tk.VERTICAL, command=self.detalles_tree.yview)
        self.detalles_tree.configure(yscrollcommand=detalles_scrollbar.set)

        # Empaquetar Treeview y scrollbar de detalles
        self.detalles_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        detalles_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Vincular evento de selección
        self.facturas_tree.bind('<<TreeviewSelect>>', self.mostrar_detalles_factura)

        # Cargar facturas
        self.cargar_facturas()

    def cargar_facturas(self):
        # Limpiar el Treeview
        for item in self.facturas_tree.get_children():
            self.facturas_tree.delete(item)

        try:
            # Obtener facturas del servicio
            facturas = self.service.obtener_facturas()
            
            # Insertar cada factura en el Treeview
            for factura in facturas:
                self.facturas_tree.insert('', 'end', values=(
                    factura['id'],
                    factura['cliente_nombre'],
                    factura['fecha'],
                    f"${factura['total']:.2f}"
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar las facturas: {str(e)}")

    def mostrar_detalles_factura(self, event):
        # Limpiar detalles anteriores
        for item in self.detalles_tree.get_children():
            self.detalles_tree.delete(item)

        # Obtener la factura seleccionada
        seleccion = self.facturas_tree.selection()
        if not seleccion:
            return

        try:
            # Obtener el ID de la factura seleccionada
            factura_id = self.facturas_tree.item(seleccion[0])['values'][0]
            
            # Obtener detalles de la factura
            detalles = self.service.obtener_detalles_factura(factura_id)
            
            # Mostrar los detalles
            for detalle in detalles:
                self.detalles_tree.insert('', 'end', values=(
                    detalle['perfume_nombre'],
                    detalle['cantidad'],
                    f"${detalle['precio_unitario']:.2f}",
                    f"${detalle['subtotal']:.2f}"
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los detalles: {str(e)}")