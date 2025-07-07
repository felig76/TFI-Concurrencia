import dal
import datetime
import threading
import queue as q
import random
import time

class Repartidor(threading.Thread):
    def __init__(self, id, nombre, estado, cola):
        self.id = id
        self.nombre = nombre
        self.estado = estado
        self.cola = cola
        self.pedido = None
    
    
    def tomar_pedido(self):
        self.pedido = self.cola.get()
        self.pedido.estado = 'En camino'
        dal.actualizar_pedido(self.pedido.cliente, self.pedido.direccion, self.pedido.estado)
        self.estado = 'Ocupado'
        dal.actualizar_repartidor(self.id, self.estado)
        time.sleep(random.randint(1, 5))
        self.entregar_pedido()


    def entregar_pedido(self):
        self.pedido.estado = 'Entregado'
        dal.actualizar_pedido(self.pedido.cliente, self.pedido.direccion, self.pedido.estado)
        self.estado = 'Disponible'
        dal.actualizar_repartidor(self.id, self.estado)


class Pedido():
    def __init__(self, cliente, direccion, estado, fecha_pedido):
        self.cliente = cliente
        self.direccion = direccion
        self.estado = estado
        self.fecha_pedido = fecha_pedido

class ColaPedidos(q.Queue):
    def __init__(self):
        super().__init__()

class ColaRepartidores(q.Queue):
    def __init__(self):
        super().__init__()

def repartidores():
    return dal.repartidores_disponibles()

def cargar_pedido(cliente, direccion):
    ColaPedidos.put(Pedido(cliente, direccion, estado='En preparación', fecha_pedido=datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")))

    dal.insertar_pedido(cliente, direccion, estado='En preparación', fecha_pedido=datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

def cargar_cliente(nombre, telefono, email):
    id_cliente = dal.cliente_existe(telefono)
    if not id_cliente:
        dal.insertar_cliente(nombre, telefono, email)
        id_cliente = dal.cliente_existe(telefono, email)
    return id_cliente

def obtener_pedidos():
    return (dal.obtener_pedidos())


def bucle_monitor():
    colaPedidos = ColaPedidos()
    for repartidor in repartidores():
        repartidor = Repartidor(repartidor[0], repartidor[1], repartidor[2], colaPedidos)
    while True:
        if not colaPedidos.empty():

