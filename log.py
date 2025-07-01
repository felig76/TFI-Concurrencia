import dal
import datetime
import threading



dal.insertar_repartidor('Joseph', 'disponible')

repartidores = dal.repartidores_disponibles()
print(repartidores)

def cargar_pedido(pedido, direccion):
    dal.insertar_pedido(cliente, direccion, estado='en camino', fecha_pedido=datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

