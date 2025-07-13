import dal
import datetime
import threading
import random
import time

class Repartidor(threading.Thread):
    def __init__(self, id, nombre, estado, cola):
        super().__init__()
        self.id = id
        self.nombre = nombre
        self.estado = estado
        self.cola = cola
        self.pedido = None

    def run(self):
        while True:
            if self.cola.qsize() > 0 and self.estado == 'disponible':
                self.tomar_pedido()
            else:
                time.sleep(2)

    def tomar_pedido(self):
        self.pedido = self.cola.get()
        self.pedido.estado = 'en camino'
        print(f"El repartidor {self.id} ha tomado el pedido {self.pedido.id}")
        dal.actualizar_pedido(self.pedido.id, self.pedido.estado)
        self.estado = 'ocupado'
        dal.actualizar_repartidor(self.id, self.estado)
        time.sleep(random.randint(5, 15))
        self.entregar_pedido()

    def entregar_pedido(self):
        self.pedido.estado = 'entregado'
        dal.actualizar_pedido(self.pedido.id, self.pedido.estado)
        print(f"El repartidor {self.id} ha entregado el pedido {self.pedido.id}")
        self.estado = 'disponible'
        dal.actualizar_repartidor(self.id, self.estado)

class Pedido():
    def __init__(self, id_pedido, cliente, direccion, estado, fecha_pedido):
        self.id = id_pedido
        self.cliente = cliente
        self.direccion = direccion
        self.estado = estado
        self.fecha_pedido = fecha_pedido

def repartidores():
    return dal.obtener_repartidores()

def cargar_pedido(cliente, direccion, colaPedidos):
    fecha = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    estado = 'en preparación'
    id_pedido = dal.insertar_pedido(cliente, direccion, estado, fecha)
    colaPedidos.put(Pedido(id_pedido, cliente, direccion, estado, fecha))

def cargar_cliente(nombre, telefono, email):
    id_cliente = dal.cliente_existe(telefono, email)
    if not id_cliente:
        dal.insertar_cliente(nombre, telefono, email)
        id_cliente = dal.cliente_existe(telefono, email)
    return id_cliente

def obtener_pedidos():
    return dal.obtener_pedidos()

def bucle_monitor(colaPedidos):
    pedidos = obtener_pedidos()
    for p in pedidos:
        colaPedidos.put(Pedido(p[0], p[1], p[2], p[3], p[4]))

    for id, nombre, estado in repartidores():
        repartidor = Repartidor(id, nombre, estado, colaPedidos)
        repartidor.daemon = True
        repartidor.start()
