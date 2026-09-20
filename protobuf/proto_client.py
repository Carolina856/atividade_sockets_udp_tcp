import random
import socket
import time
import calc_pb2
import threading

PORT = 6789
HOST = 'localhost'

N_REQ = 20
N_CLIENTS = 1

operadores = ['+', '-', '*', '/']

def execute_client(num):
    rtt = []
    tam = []

    # Cada thread possui sua própria conexão
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    inicio_total = time.perf_counter()
    ultimo_tempo = inicio_total

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
        print(f"Cliente {num} - Tamanho dos dados em bytes: {len(data)}")
        tam.append(len(data))
        ultimo_tempo = time.perf_counter()
        s.sendall(data)
        print(f"Cliente {num} - Mensagem {n} enviada para o servidor. Aguardando resposta.")
    
        data_rcv = s.recv(1024)

        agora = time.perf_counter()
        tempo_req = agora - ultimo_tempo
        rtt.append(tempo_req)

        msg_rcv = calc_pb2.CalcResult()
        msg_rcv.ParseFromString(data_rcv)
        print(f"Cliente {num} - {msg_rcv.status}:{msg_rcv.n_seq}:{msg_rcv.result}")

    fim_total = time.perf_counter()
    tempo_total = fim_total - inicio_total

    s.close()

    # Resultados do cliente
    sum_rtt = 0
    #print(f"\nCliente {num} - Tempo de cada RTT (em segundos)")
    for i in range(N_REQ):
        #print(f"{i}: {rtt[i]}")
        sum_rtt += rtt[i]
    print(f"\nCliente {num} - RTT médio (ms): {(sum_rtt/N_REQ * 1000):.3f}")
    print(f"Cliente {num} - RTT máximo (ms): {(max(rtt) * 1000):.3f}")
    print(f"Cliente {num} - Tempo total (ms): {(tempo_total * 1000):.3f}")

    sum_tam = 0
    #print(f"\nCliente {num} - Tamanho das mensagens:")
    for i in range(N_REQ):
        sum_tam += tam[i]
        #print(f"Cliente {num} - Mensagem {i}: {tam[i]}")
    print(f"Cliente {num} - Tamanho médio: {(sum_tam/N_REQ):.3f}")
       
# Criação das threads
threads = []
inicio_concorrencia = time.perf_counter()

for i in range(N_CLIENTS):

    thread = threading.Thread(
        target=execute_client,
        args=(i + 1,)
    )

    threads.append(thread)
    thread.start()

# Espera todas as threads terminarem
for thread in threads:
    thread.join()

fim_concorrencia = time.perf_counter()

print(
    f"\nTempo total da execução concorrente: "
    f"{(fim_concorrencia - inicio_concorrencia) * 1000:.3f} ms"
)

