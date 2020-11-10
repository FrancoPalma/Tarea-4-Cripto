from Crypto.Cipher import PKCS1_OAEP
import Crypto
from Crypto.PublicKey import RSA
import socket
import time
import binascii
import os
import time
import sys
import hashlib
if sys.version_info < (3, 6):
    import sha3

#Crackeamos los hash que se encuentran en archivos
os.chdir('hashcat-6.1.1')
f = open ('tiempos.txt','w')
start_time = time.time()

os.system('hashcat.exe -m0 -a0 archivo_1 diccionario_1.dict diccionario_2.dict --force --outfile-format=2 -o out1.txt') #MD5
time1 = time.time() - start_time
f.write("Segundos Archivo 1: "+str(time1)+"\n")
start_time = time.time()

os.system('hashcat.exe -m10 -a0 archivo_2 diccionario_1.dict diccionario_2.dict --force --outfile-format=2 -o out2.txt') #md5($pass.$salt)
time2 = time.time() - start_time
f.write("Segundos Archivo 2: "+str(time2)+"\n")
start_time = time.time()

os.system('hashcat.exe -m10 -a0 archivo_3 diccionario_1.dict diccionario_2.dict --force --outfile-format=2 -o out3.txt') #md5($pass.$salt)
time3 = time.time() - start_time
f.write("Segundos Archivo 3: "+str(time3)+"\n")
start_time = time.time()

os.system('hashcat.exe -m1000 -a0 archivo_4 diccionario_1.dict diccionario_2.dict --force --outfile-format=2 -o out4.txt') #NTLM
time4 = time.time() - start_time
f.write("Segundos Archivo 4: "+str(time4)+"\n")
start_time = time.time()

os.system('hashcat.exe -m1800 -a0 archivo_5 diccionario_1.dict diccionario_2.dict --force --outfile-format=2 -o out5.txt') #sha512crypt $6$, SHA512 (Unix)
time5 = time() - start_time
f.write("Segundos Archivo 5: "+str(time5)+"\n")

f.close()

#Se conecta con el servidor
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 8000))

# Se recibe la key publica
s.send("Clave por favor.".encode())
public_key = s.recv(1000).decode()
public_key = RSA.importKey(binascii.unhexlify(public_key))
cipher = PKCS1_OAEP.new(public_key)

f = open("out1.txt",'r')
lineas = f.readlines()
s.send(str(len(lineas)).encode())

for i in lineas:
    encrypted_message  = cipher.encrypt((hashlib.sha3_256((i.encode())).hexdigest()).encode())
    s.send(encrypted_message)
    confirmacion = s.recv(1000).decode()
    print(confirmacion)
f.close()

del(lineas)
f = open("out2.txt",'r')
lineas = f.readlines()
s.send(str(len(lineas)).encode())

for i in lineas:
    encrypted_message  = cipher.encrypt((hashlib.sha3_256((i.encode())).hexdigest()).encode())
    s.send(encrypted_message)
    confirmacion = s.recv(1000).decode()
    print(confirmacion)
f.close()
del(lineas)

f = open("out3.txt",'r')
lineas = f.readlines()
s.send(str(len(lineas)).encode())

for i in lineas:
    encrypted_message  = cipher.encrypt((hashlib.sha3_256((i.encode())).hexdigest()).encode())
    s.send(encrypted_message)
    confirmacion = s.recv(1000).decode()
    print(confirmacion)
f.close()
del(lineas)

f = open("out4.txt",'r')
lineas = f.readlines()
s.send(str(len(lineas)).encode())

for i in lineas:
    encrypted_message  = cipher.encrypt((hashlib.sha3_256((i.encode())).hexdigest()).encode())
    s.send(encrypted_message)
    confirmacion = s.recv(1000).decode()
    print(confirmacion)
f.close()
del(lineas)

f = open("out5.txt",'r')
lineas = f.readlines()
s.send(str(len(lineas)).encode())

for i in lineas:
    encrypted_message  = cipher.encrypt((hashlib.sha3_256((i.encode())).hexdigest()).encode())
    s.send(encrypted_message)
    confirmacion = s.recv(1000).decode()
    print(confirmacion)
f.close()
del(lineas)

s.close()
