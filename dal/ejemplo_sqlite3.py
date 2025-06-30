import sqlite3

try:
    #conn = sqlite3.connect(r"C:\Users\Marcos\Desktop\Et\2023\dbschuff.db")
    conn = sqlite3.connect(r"C:\Users\Marcos\Desktop\Et\2023\python-sqlite.db")
    c=conn.cursor()
except Exception as ex:
    print(ex)

lista1=[]       #"var" cambiable
lista2=[]       #"var" cambiable

c.execute("CREATE TABLE IF NOT EXISTS tabla1 (id_lista INTEGER, lista1 TEXT, lista2 TEXT)")

def ingresar():
        salida="si"
        while salida=="si":
            var1=str(input("Ingrese elemento1 : "))     #"elemento" cambiable
            var2=str(input("Ingrese elemento2 : "))     #"elemento" cambiable
            lista1.append(var1)     #"var" cambiable
            lista2.append(var2)     #"var" cambiable
            salida=str(input("Desea seguir ingresando? (si/no): "))

        for campo1, campo2 in zip(lista1, lista2):
            pk=next_pk()
            lista_db=[pk, campo1, campo2]       #"var" cambiable
            c.execute(f"INSERT INTO tabla1 VALUES (?, ?, ?)", lista_db)
            conn.commit()

def next_pk():
    c.execute(f"SELECT MAX(id_lista) FROM 'tabla1'")    #busca ultimo id(pk) de la tabla
    result = c.fetchone()
    conn.commit()
    if result[0] is None:
        return 1
    else:
        return result[0] + 1

def eliminar():
    id_eliminar=int(input("ingrese el id del registro que quiera eliminar"))     #num de id(pk) del registro a eliminar
    c.execute(f"DELETE FROM tabla1 WHERE id_lista = ?", (id_eliminar))
    conn.commit()

while True:
    operacion=int(input("""¿QUE ES LO QUE DESEA HACER? 
                            1-VER
                            2-INGRESAR
                            3-ELIMINAR
                            0-SALIR
                            """))
    match operacion:
        #case 1:
            #mostrar_lista()
        case 2:
            ingresar()
        case 3:
            eliminar()
        case 0:
            break

conn.commit()
conn.close()
