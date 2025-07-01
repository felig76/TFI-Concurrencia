import log

# cajas de texto para logear clientes -> insertar en caso que no exista -> devolver id
def nuevo_cliente(nombre, telefono, email):
    id_cliente = log.cargar_cliente(nombre, telefono, email)

def nuevo_pedido(id_cliente, direccion):
    log.cargar_pedido(id_cliente, direccion)
