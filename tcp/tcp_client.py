import random
import socket
import time

PORT = 6789
HOST = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

operadores = ['+', '-', '*', '/']
rtt = []

inicio = time.perf_counter()
ultimo_tempo = inicio

for n in range(20):
    num1 = random.randint(0, 100)
    num2 = random.randint(0, 100)
    op = random.choice(operadores)

    msg = "CALC:" + str(n) + ":" + str(num1) + ":" + op + ":" + str(num2)
    print(msg)
    s.sendall(bytes(msg, 'utf-8'))
    data = s.recv(1024).decode('utf-8')
    print(f"{data}\n")

    agora = time.perf_counter()
    tempo_req = agora - ultimo_tempo
    ultimo_tempo = agora
    rtt.append(tempo_req)

agora = time.perf_counter()
tempo_total = agora - inicio
s.close()

sum = 0
print("Tempo de cada RTT (em segundos)")
for i in range(20):
    print(f"{i}: {rtt[i]}")
    sum += rtt[i]
print(f"\nRTT médio (em segundos): {sum/20}")
print(f"RTT máximo (em segundos): {max(rtt)}")
print(f"Tempo total (em segundos): {tempo_total}")