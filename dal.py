import sqlite3

def conexion(query, params=(), fetch=False):
    try:
        conn = sqlite3.connect(r"./db.db")
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

def obtener_pedidos():
    return conexion("SELECT * FROM Pedidos", fetch=True)

def cliente_existe(telefono, email):
    result = conexion("SELECT id FROM Clientes WHERE telefono = ? AND email = ?", (telefono, email), fetch=True)
    return result[0][0] if result else None

def insertar_cliente(nombre, telefono, email):
    conexion("INSERT INTO Clientes (nombre, telefono, email) VALUES (?, ?, ?)", (nombre, telefono, email))

def actualizar_pedido(cliente, direccion, estado):
    conexion("UPDATE Pedidos SET estado = ? WHERE cliente = ? AND direccion = ?", (estado, cliente, direccion))

def actualizar_repartidor(id, estado):
    conexion("UPDATE Repartidores SET estado = ? WHERE id = ?", (estado, id))