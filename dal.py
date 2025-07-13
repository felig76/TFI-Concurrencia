import sqlite3

def conexion(query, params=(), fetch=False, return_last_id=False):
    try:
        conn = sqlite3.connect(r"./db.db")
        c = conn.cursor()
        c.execute(query, params)

        if fetch:
            result = c.fetchall()
        elif return_last_id:
            result = c.lastrowid
        else:
            result = None

        conn.commit()
        conn.close()

        return result
    except Exception as ex:
        print("Error en conexión:", ex)
        return None

def insertar_repartidor(nombre, estado):
    conexion("INSERT INTO Repartidores (nombre, estado) VALUES (?, ?)", (nombre, estado))

def obtener_repartidores():
    return conexion("SELECT * FROM Repartidores", fetch=True)

def insertar_pedido(cliente, direccion, estado, fecha_pedido):
    return conexion(
        "INSERT INTO Pedidos (cliente, direccion, estado, fecha_pedido) VALUES (?, ?, ?, ?)",
        (cliente, direccion, estado, fecha_pedido),
        return_last_id=True
    )

def obtener_pedidos():
    return conexion("SELECT * FROM Pedidos WHERE estado != 'entregado'", fetch=True)

def cliente_existe(telefono, email):
    result = conexion("SELECT id FROM Clientes WHERE telefono = ? AND email = ?", (telefono, email), fetch=True)
    return result[0][0] if result else None

def insertar_cliente(nombre, telefono, email):
    conexion("INSERT INTO Clientes (nombre, telefono, email) VALUES (?, ?, ?)", (nombre, telefono, email))

def actualizar_pedido(id_pedido, estado):
    conexion("UPDATE Pedidos SET estado = ? WHERE id = ?", (estado, id_pedido))

def actualizar_repartidor(id, estado):
    conexion("UPDATE Repartidores SET estado = ? WHERE id = ?", (estado, id))
