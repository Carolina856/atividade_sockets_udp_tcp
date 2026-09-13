import random
import socket
import time

PORT = 6789
HOST = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

operadores = ['+', '-', '*', '/']
rtt = []

for n in range(20):
    num1 = random.randint(0, 100)
    num2 = random.randint(0, 100)
    op = random.choice(operadores)

    msg = "CALC:" + str(n) + ":" + str(num1) + ":" + op + ":" + str(num2)
    print(msg)
    inicio = time.perf_counter()

    s.sendall(bytes(msg, 'utf-8'))
    data = s.recv(1024).decode('utf-8')
    print ('{s}\n'.format(s=repr(data)))
    fim = time.perf_counter()

    tempo = fim - inicio
    rtt.append(tempo)

s.close()

print("Tempo de cada RTT")
for i in range(20):
    print(f"{i}: {rtt[i]}")