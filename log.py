import dal
import datetime
import threading

def repartidores():
    return dal.repartidores_disponibles()

def cargar_pedido(cliente, direccion):
    dal.insertar_pedido(cliente, direccion, estado='en camino', fecha_pedido=datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

def cargar_cliente(nombre, telefono, email):
    id_cliente = dal.cliente_existe(telefono)
    if not id_cliente:
        dal.insertar_cliente(nombre, telefono, email)
        id_cliente = dal.cliente_existe(telefono)
    return id_cliente
