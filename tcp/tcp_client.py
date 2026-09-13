import socket
import random

PORT = 6789
HOST = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

num1 = random.randint(0, 100)
num2 = random.randint(0, 100)

operadores = ['+', '-', '*', '/']
op = random.choice(operadores)
print(f"Número 1: {num1}")
print(f"Número 2: {num2}")
print(f"Operador: {op}")
msg = "CALC:" + str(num1) + ":" + op + ":" + str(num2)
print(msg)

s.sendall(bytes(msg, 'utf-8'))
data = s.recv(1024).decode('utf-8')
s.close()
print ('FROM SERVER: {s}'.format(s=repr(data)))