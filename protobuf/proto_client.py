import random
import socket
import time
import calc_pb2

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

    msg = calc_pb2.CalcRequest()

    msg.n_seq = n
    msg.operando1 = num1
    msg.op = op
    msg.operando2 = num2

    data = msg.SerializeToString()
    inicio = time.perf_counter()
    s.sendall(data)
    print(f"Mensagem {n} enviada para o servidor. Aguardando resposta.")

    data_rcv = s.recv(1024)
    msg_rcv = calc_pb2.CalcResult()
    msg_rcv.ParseFromString(data_rcv)
    
    print(f"{msg_rcv.status}:{msg_rcv.n_seq}:{msg_rcv.result}")
    fim = time.perf_counter()

    tempo = fim - inicio
    rtt.append(tempo)

s.close()

print("\nTempo de cada RTT")
for i in range(20):
    print(f"{i}: {rtt[i]}")