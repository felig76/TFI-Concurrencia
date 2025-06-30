import sqlite3

try:
    conn = sqlite3.connect(r"C:\Users\Marcos\Desktop\Et\2025\programacionsobreredes\programacion_concurrente\TFI-CONCURRENCIA\db.db")
    c = conn.cursor()

except Exception as ex:
    print(ex)

c.execute("INSERT INTO Repartidores VALUES (1, 'Natanael', 'disponible')")

conn.commit()

conn.close()
