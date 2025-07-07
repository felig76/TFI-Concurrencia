import tkinter as tk
from tkinter import ttk
import log

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Pedidos")
        self.geometry("400x500")
        self.resizable(False, False)

        self.cliente_id = None

        self.frame_login = ttk.Frame(self)
        self.frame_pedidos = ttk.Frame(self)

        self.crear_vista_login()
        self.crear_vista_pedidos()

        self.mostrar_login()

    def crear_vista_login(self):
        # Widgets para login
        self.entry_nombre = ttk.Entry(self.frame_login)
        self.entry_nombre.insert(0, "Nombre")
        self.entry_telefono = ttk.Entry(self.frame_login)
        self.entry_telefono.insert(0, "Teléfono")
        self.entry_email = ttk.Entry(self.frame_login)
        self.entry_email.insert(0, "Email")
        self.boton_login = ttk.Button(self.frame_login, text="Iniciar sesión", command=self.login_cliente)

        # Posicionamiento centrado vertical
        for widget in [self.entry_nombre, self.entry_telefono, self.entry_email, self.boton_login]:
            widget.pack(pady=10, ipadx=20)

    def crear_vista_pedidos(self):
        # Dirección para generar pedido
        self.entry_direccion = ttk.Entry(self.frame_pedidos)
        self.entry_direccion.insert(0, "Dirección de entrega")
        self.entry_direccion.pack(pady=10, padx=20, fill='x')

        # Botón para generar pedido
        self.boton_pedido = ttk.Button(self.frame_pedidos, text="Generar pedido", command=self.generar_pedido)
        self.boton_pedido.pack(pady=10)

        # Lista de repartidores
        self.label_repartidores = ttk.Label(self.frame_pedidos, text="Repartidores disponibles:")
        self.label_repartidores.pack()

        self.lista_repartidores = tk.Listbox(self.frame_pedidos, height=10)
        self.lista_repartidores.pack(fill='both', expand=True, padx=20, pady=10)

        # Botón para cerrar sesión
        self.boton_logout = ttk.Button(self.frame_pedidos, text="Cerrar sesión", command=self.logout)
        self.boton_logout.pack(pady=10)

    def mostrar_login(self):
        self.frame_pedidos.pack_forget()
        self.frame_login.pack(expand=True)

    def mostrar_pedidos(self):
        self.frame_login.pack_forget()
        self.actualizar_repartidores()
        self.frame_pedidos.pack(expand=True, fill="both")

    def login_cliente(self):
        nombre = self.entry_nombre.get()
        telefono = self.entry_telefono.get()
        email = self.entry_email.get()

        self.cliente_id = log.cargar_cliente(nombre, telefono, email)

        if self.cliente_id:
            self.mostrar_pedidos()
        else:
            print("Error al iniciar sesión")

    def generar_pedido(self):
        direccion = self.entry_direccion.get()
        if self.cliente_id and direccion:
            log.cargar_pedido(self.cliente_id, direccion)
            print("Pedido generado")
            self.actualizar_repartidores()

    def actualizar_repartidores(self):
        repartidores = log.repartidores()
        self.lista_repartidores.delete(0, tk.END)
        for r in repartidores:
            self.lista_repartidores.insert(tk.END, f"{r[1]} - {r[2]}")  # nombre - estado

    def logout(self):
        self.cliente_id = None
        self.entry_nombre.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_direccion.delete(0, tk.END)
        self.mostrar_login()


if __name__ == "__main__":
    app = App()
    app.mainloop()