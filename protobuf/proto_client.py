import random
import socket
import time
import calc_pb2

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

    msg = calc_pb2.CalcRequest()

    msg.n_seq = n
    msg.operando1 = num1
    msg.op = op
    msg.operando2 = num2

    data = msg.SerializeToString()
    print(f"Tamanho dos dados em bytes: {len(data)}")
    tam.append(len(data))
    inicio = time.perf_counter()
    s.sendall(data)
    print(f"Mensagem {n} enviada para o servidor. Aguardando resposta.")

    data_rcv = s.recv(1024)
    msg_rcv = calc_pb2.CalcResult()
    msg_rcv.ParseFromString(data_rcv)
    print(f"{msg_rcv.status}:{msg_rcv.n_seq}:{msg_rcv.result}")

    agora = time.perf_counter()
    tempo_req = agora - ultimo_tempo
    ultimo_tempo = agora
    rtt.append(tempo_req)

agora = time.perf_counter()
tempo_total = agora - inicio
s.close()

sum_rtt = 0
print("\nTempo de cada RTT (em segundos)")
for i in range(N_REQ):
    print(f"{i}: {rtt[i]}")
    sum_rtt += rtt[i]
print(f"\nRTT médio (em segundos): {(sum_rtt/N_REQ * 1000):.3f}")
print(f"RTT máximo (em segundos): {(max(rtt) * 1000):.3f}")
print(f"Tempo total (em segundos): {(sum_rtt * 1000):.3f}")

sum_tam = 0
print("\nTamanho das mensagens:")
for i in range(N_REQ):
    sum_tam += tam[i]
    print(f"Mensagem {i}: {tam[i]}")
print(f"Tamanho médio: {(sum_tam/N_REQ):.3f}")