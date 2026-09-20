import socket
import threading
import time
import random

PORT = 6789
HOST = 'localhost'

N_REQ = 20
N_CLIENTS = 1

operadores = ['+', '-', '*', '/']
threads = []

def execute_client(num):
    rtt = []
    tam = []

    inicio_total = time.perf_counter()
    ultimo_tempo = inicio_total

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        for i in range(N_REQ):
            num1 = random.randint(0, 100)
            num2 = random.randint(0, 100)
            op = random.choice(operadores)

            msg = "CALC:" + str(i) + ":" + str(num1) + ":" + op + ":" + str(num2)
            print(msg)
            msg_b = bytes(msg, 'utf-8')
            tam.append(len(msg_b))
            ultimo_tempo = time.perf_counter()
            s.sendall(msg_b)
            data = s.recv(1024).decode('utf-8')
            print(f"Client: {num} - Mensagem {i + 1}: {data}")

            agora = time.perf_counter()
            tempo_req = agora - ultimo_tempo
            rtt.append(tempo_req)

        agora = time.perf_counter()
        tempo_total = agora - inicio_total

        sum_rtt = 0
        print(f"Cliente {num} - Tempo de cada RTT (em segundos)")
        for i in range(N_REQ):
            print(f"{i}: {rtt[i]}")
            sum_rtt += rtt[i]
        print(f"\nCliente {num} - RTT médio (ms): {(sum_rtt/N_REQ * 1000):.3f}")
        print(f"Cliente {num} - RTT máximo (ms): {(max(rtt) * 1000):.3f}")
        print(f"Cliente {num} - Tempo total (ms): {(tempo_total * 1000):.3f}")

        sum_tam = 0
       # print(f"\nCliente {num} - Tamanho de cada mensagem")
        for i in range(N_REQ):
            #print(f"Mensagem {i}: {tam[i]}")
            sum_tam += tam[i]
        print(f"Cliente {num} - Tamanho médio das mensagens: {(sum_tam/N_REQ):.3f}")

inicio_concorrencia = time.perf_counter()

for i in range(N_CLIENTS):
    thread = threading.Thread(
        target=execute_client,
        args=(i + 1,)
    )

    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

fim_concorrencia = time.perf_counter()

print(f"\nTempo total: {fim_concorrencia - inicio_concorrencia:.2f} segundos")
