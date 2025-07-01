import sqlite3

def conexion(query, params=(), fetch=False):
    try:
        conn = sqlite3.connect(r"../TFI-CONCURRENCIA/db.db")
        c = conn.cursor()
        c.execute(query, params)
        
        result = c.fetchall() if fetch else None
        conn.commit()
        conn.close()
        return result
    except Exception as ex:
        print("Error en conexión:", ex)
        return None


def insertar_repartidor(nombre, estado):
    conexion("INSERT INTO Repartidores (nombre, estado) VALUES (?, ?)", (nombre, estado))

def repartidores_disponibles():
    return conexion("SELECT * FROM Repartidores WHERE estado = ?", ('disponible',), fetch=True)


def insertar_pedido(cliente, direccion, estado, fecha_pedido):
    conexion(
        "INSERT INTO Pedidos (cliente, direccion, estado, fecha_pedido) VALUES (?, ?, ?, ?)",
        (cliente, direccion, estado, fecha_pedido)
    )

def cliente_existe(telefono):
    result = conexion("SELECT id_cliente FROM Clientes WHERE telefono = ?", (telefono,), fetch=True)
    return result[0][0] if result else None

# select pedidos


# insert y select historial


# logica de asignaciones
