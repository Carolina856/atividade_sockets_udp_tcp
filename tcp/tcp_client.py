import random
import socket
import time

PORT = 6789
HOST = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

N_REQ = 20

operadores = ['+', '-', '*', '/']
rtt = []
tam = []

inicio = time.perf_counter()
ultimo_tempo = inicio

for n in range(N_REQ):
    num1 = random.randint(0, 100)
    num2 = random.randint(0, 100)
    op = random.choice(operadores)

    msg = "CALC:" + str(n) + ":" + str(num1) + ":" + op + ":" + str(num2)
    print(msg)
    msg_b = bytes(msg, 'utf-8')
    tam.append(len(msg_b))
    s.sendall(msg_b)
    data = s.recv(1024).decode('utf-8')
    print(f"{data}\n")

    agora = time.perf_counter()
    tempo_req = agora - ultimo_tempo
    ultimo_tempo = agora
    rtt.append(tempo_req)

agora = time.perf_counter()
tempo_total = agora - inicio
s.close()

sum_rtt = 0
print("Tempo de cada RTT (em segundos)")
for i in range(N_REQ):
    print(f"{i}: {rtt[i]}")
    sum_rtt += rtt[i]
print(f"\nRTT médio (ms): {(sum_rtt/N_REQ * 1000):.3f}")
print(f"RTT máximo (ms): {(max(rtt) * 1000):.3f}")
print(f"Tempo total (ms): {(tempo_total * 1000):.3f}")

sum_tam = 0
print("\nTamanho de cada mensagem")
for i in range(N_REQ):
    print(f"Mensagem {i}: {tam[i]}")
    sum_tam += tam[i]
print(f"Tamanho médio das mensagens: {(sum_tam/N_REQ):.3f}")