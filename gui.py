import tkinter as tk
from tkinter import ttk
import log
import queue as q
import threading

class ColaPedidos(q.Queue):
    def __init__(self):
        super().__init__()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Pedidos")
        self.geometry("550x650")
        self.resizable(False, False)
        self.modo_actual = "claro"

        self.fuente_general = ("Segoe UI", 11)
        self.fuente_entry = ("Consolas", 14)

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.crear_estilos_claros()

        self.crear_vista_principal()

        self.colaPedidos = ColaPedidos()

    def crear_estilos_claros(self):
        self.style.configure("TFrame", background="#EAEAEA")
        self.style.configure("TLabel", font=self.fuente_general, background="#EAEAEA", foreground="#333")
        self.style.configure("TButton", font=self.fuente_general, background="#2C3E50", foreground="white", padding=8, relief="flat")
        self.style.map("TButton", background=[("active", "#1A252F")])

    def crear_estilos_oscuro(self):
        self.style.configure("TFrame", background="#121212")
        self.style.configure("TLabel", font=self.fuente_general, background="#121212", foreground="#EAEAEA")
        self.style.configure("TButton", font=self.fuente_general, background="#3D9970", foreground="#FFFFFF", padding=8, relief="flat")
        self.style.map("TButton", background=[("active", "#2E7D5F")])

    def crear_vista_principal(self):
        top_frame = ttk.Frame(self, style="TFrame")
        top_frame.pack(fill='x', anchor='n', padx=10, pady=(10, 0))

        self.boton_modo = ttk.Button(top_frame, text="Oscuro", command=self.toggle_modo, width=10)
        self.boton_modo.pack(anchor='ne')

        frame = ttk.Frame(self, style="TFrame")
        frame.pack(expand=True, fill="both", padx=20, pady=(20, 20))

        self.entry_nombre = ttk.Entry(frame, font=self.fuente_entry)
        self.agregar_placeholder(self.entry_nombre, "Nombre")
        self.entry_nombre.pack(pady=5, ipadx=20, fill='x')

        self.entry_telefono = ttk.Entry(frame, font=self.fuente_entry)
        self.agregar_placeholder(self.entry_telefono, "Teléfono")
        self.entry_telefono.pack(pady=5, ipadx=20, fill='x')

        self.entry_email = ttk.Entry(frame, font=self.fuente_entry)
        self.agregar_placeholder(self.entry_email, "Email")
        self.entry_email.pack(pady=5, ipadx=20, fill='x')

        self.entry_direccion = ttk.Entry(frame, font=self.fuente_entry)
        self.agregar_placeholder(self.entry_direccion, "Dirección de entrega")
        self.entry_direccion.pack(pady=10, fill='x')

        self.boton_pedido = ttk.Button(frame, text="Generar pedido", command=self.generar_pedido)
        self.boton_pedido.pack(pady=10, fill='x')

        self.label_repartidores = ttk.Label(frame, text="Repartidores disponibles:")
        self.label_repartidores.pack(anchor='w')

        self.lista_repartidores = tk.Listbox(frame, height=5)
        self.lista_repartidores.pack(fill='both', expand=False, pady=10)

        self.label_pedidos = ttk.Label(frame, text="Pedidos en curso:")
        self.label_pedidos.pack(anchor='w')

        self.lista_pedidos = tk.Listbox(frame, height=10)
        self.lista_pedidos.pack(fill='both', expand=True, pady=10)

        self.actualizar_repartidores()
        self.actualizar_pedidos()
        self.after(100, self.actualizar_periodicamente)

    def agregar_placeholder(self, entry, placeholder):
        entry.insert(0, placeholder)
        entry.config(foreground='grey')

        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(foreground='black')

        def on_focus_out(event):
            if entry.get() == '':
                entry.insert(0, placeholder)
                entry.config(foreground='grey')

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def generar_pedido(self):
        nombre = self.entry_nombre.get()
        telefono = self.entry_telefono.get()
        email = self.entry_email.get()
        direccion = self.entry_direccion.get()
        colaPedidos = self.colaPedidos

        if nombre in ["Nombre", ""] or telefono in ["Teléfono", ""] or email in ["Email", ""] or direccion in ["Dirección de entrega", ""]:
            print("Completa todos los campos")
            return

        cliente_id = log.cargar_cliente(nombre, telefono, email)

        if cliente_id:
            log.cargar_pedido(cliente_id, direccion, colaPedidos)
            print("Pedido generado")
            self.actualizar_repartidores()
            self.actualizar_pedidos()
            self.limpiar_campos()
        else:
            print("Error al cargar cliente")

    def actualizar_repartidores(self):
        repartidores = log.repartidores()
        self.lista_repartidores.delete(0, tk.END)
        for r in repartidores:
            self.lista_repartidores.insert(tk.END, f"{r[1]} - {r[2]}")

    def actualizar_pedidos(self):
        pedidos = log.obtener_pedidos()
        self.lista_pedidos.delete(0, tk.END)
        for p in pedidos:
            pedido_id, cliente, direccion, estado, fecha_hora = p
            self.lista_pedidos.insert(tk.END, f"#{pedido_id}: Cliente {cliente}, {direccion} - {estado} ({fecha_hora})")

    def limpiar_campos(self):
        for entry, placeholder in [
            (self.entry_nombre, "Nombre"),
            (self.entry_telefono, "Teléfono"),
            (self.entry_email, "Email"),
            (self.entry_direccion, "Dirección de entrega")
        ]:
            entry.delete(0, tk.END)
            entry.insert(0, placeholder)
            entry.config(foreground='grey')

    def actualizar_periodicamente(self):
        self.actualizar_repartidores()
        self.actualizar_pedidos()
        self.after(2000, self.actualizar_periodicamente)

    def toggle_modo(self):
        if self.modo_actual == "claro":
            self.configure(bg="#121212")
            self.crear_estilos_oscuro()
            self.modo_actual = "oscuro"
            self.boton_modo.config(text="Claro")
        else:
            self.configure(bg="#EAEAEA")
            self.crear_estilos_claros()
            self.modo_actual = "claro"
            self.boton_modo.config(text="Oscuro")

if __name__ == "__main__":
    app = App()
    monitor_thread = threading.Thread(target=log.bucle_monitor, args=(app.colaPedidos,), daemon=True)
    monitor_thread.start()
    app.mainloop()
