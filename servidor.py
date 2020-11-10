from Crypto.Cipher import PKCS1_OAEP
import Crypto
from Crypto.PublicKey import RSA
import socket
import time
import binascii
import sqlite3
from sqlite3 import Error

#Funciones para la base de datos
def sql_connection():
    try:
        con = sqlite3.connect('cripto.bd')
        print("Connection is established: Database is created in memory")
        return con
    except Error:
        print(Error)

def sql_table(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE HashSHA3(id integer PRIMARY KEY, Archivo_n°, Data)")
    con.commit()

def sql_insert(con, entities):
    cursorObj = con.cursor()
    cursorObj.execute('INSERT INTO HashSHA3(id, Archivo_n°, Data) VALUES(?, ?, ?)', entities)
    con.commit()

def sql_fetch(con):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM HashSHA3')
    rows = cursorObj.fetchall()
    for row in rows:
        print(row)

#Se generan las llaves del cifrado
random_generator = Crypto.Random.new().read
private_key = RSA.generate(1024, random_generator)
public_key = private_key.publickey()

#la llave publica es transformada a utf-8 para poder enviarla por un socket
public_key = public_key.exportKey(format='DER')
public_key = binascii.hexlify(public_key).decode('utf8')
cipher = PKCS1_OAEP.new(private_key)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("", 8000))
server.listen(1)

while 1:
    #se conecta con el cliente, crea una base de datos y se le envia la llave al cliente
    socket_cliente, datos_cliente = server.accept()
    print("conectado "+str(datos_cliente))
    mensaje = socket_cliente.recv(1000).decode()
    print(str(mensaje))
    con = sql_connection()
    sql_table(con)
    socket_cliente.send(public_key.encode())
    #se recibe la cantidad de hash a recibir y luego los hash
    #para luego insetarlos en la base
    lineas1 = int(socket_cliente.recv(1000).decode())
    count = 1
    for i in range(lineas1):
        encrypted_message = socket_cliente.recv(1000)
        message = cipher.decrypt(encrypted_message)
        sql_insert(con, (count,1,message.decode()))
        count += 1
        socket_cliente.send((str(count)+"Listo").encode())

    lineas2 = int(socket_cliente.recv(1000).decode())
    for i in range(lineas2):
        encrypted_message = socket_cliente.recv(1000)
        message = cipher.decrypt(encrypted_message)
        sql_insert(con, (count,2,message.decode()))
        count += 1
        socket_cliente.send((str(count)+"Listo").encode())

    lineas3 = int(socket_cliente.recv(1000).decode())
    for i in range(lineas3):
        encrypted_message = socket_cliente.recv(1000)
        message = cipher.decrypt(encrypted_message)
        sql_insert(con, (count,3,message.decode()))
        count += 1
        socket_cliente.send((str(count)+"Listo").encode())

    lineas4 = int(socket_cliente.recv(1000).decode())
    for i in range(lineas4):
        encrypted_message = socket_cliente.recv(1000)
        message = cipher.decrypt(encrypted_message)
        sql_insert(con, (count,4,message.decode()))
        count += 1
        socket_cliente.send((str(count)+"Listo").encode())

    lineas5 = int(socket_cliente.recv(1000).decode())
    for i in range(lineas5):
        encrypted_message = socket_cliente.recv(1000)
        message = cipher.decrypt(encrypted_message)
        sql_insert(con, (count,5,message.decode()))
        count += 1
        socket_cliente.send((str(count)+"Listo").encode())

sql_fetch(con)
