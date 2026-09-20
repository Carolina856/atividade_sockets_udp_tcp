import random
import socket
import time
import threading

HOST = "127.0.0.1"
PORT = 6789

N_REQ = 20
N_CLIENTS = 1

MAX_RETRANSMISSAO = 5 
MAX_TEMPO = 0.5 # Tempo máximo de espera da mensagem em segundos

operadores = ['+', '-', '*', '/']

def execute_client(num):
    resultados = []

    inicio_total = time.perf_counter()
    ultimo_tempo = inicio_total

    for n in range(N_REQ):
        #Cálculo da operação matemática aleatória
        num1 = random.randint(0, 100)
        num2 = random.randint(0, 100)
        op = random.choice(operadores)

        msg = "CALC:" + str(n) + ":" + str(num1) + ":" + op + ":" + str(num2)
        print(f"Cliente {num} - {msg}")
    
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(MAX_TEMPO) 

        recebido = False

        ultimo_tempo = time.perf_counter()
        # 1 para o primeiro envio + limite de tentativas de retransmissão da requisição
        for tentativa in range(1 + MAX_RETRANSMISSAO):
            try:
                s.sendto(bytes(msg, 'utf-8'), (HOST, PORT))
            
                if tentativa != 0:
                    print(f"Cliente {num} - Retransmissão {tentativa} da mensagem {n}")

                data = s.recv(1024).decode('utf-8')
                print(f"{data}")

                agora = time.perf_counter()
                tempo_req = agora - ultimo_tempo

                resultados.append({
                    "rtt": tempo_req,
                    "retransmissoes": tentativa
                })

                recebido = True
                break

            except TimeoutError:
                print(f"Cliente {num} - Timeout na resposta da mensagem {n}")

        # Cliente não recebeu resposta do servidor
        if recebido == False:
            print(f"Cliente {num} - Nenhuma resposta após {MAX_RETRANSMISSAO} retransmissões\n")
            resultados.append({
                "rtt": None,
                "retransmissoes": tentativa
            })

            ultimo_tempo = time.perf_counter()

        s.close()

    fim_total = time.perf_counter()
    tempo_total = fim_total - inicio_total

    # Cálculo dos RTTs
    sum = 0
    cont = 0
    perdidos = 0
    #print(f"Cliente {num} - Tempo de cada RTT (ms)")
    for i in range(N_REQ):
        #print(f"Cliente {num} - n: {i}  rtt: {(resultados[i]["rtt"] * 1000):.3f}    retransmissões:{resultados[i]["retransmissoes"]}")

        # Se o datagrama foi perdido, o rtt dele é None e ele é ignorado no cálculo do RTT médio 
        # mas o tempo dele ainda é considerado no tempo total da conexão entre o servidor e o cliente
        if resultados[i]["rtt"] != None:
            sum += resultados[i]["rtt"]
            cont += 1
        else:
            perdidos += 0

    rtts = []
    total_retransmissoes = 0
    for res in resultados:
        if res["rtt"] is not None:
            rtts.append(res["rtt"])
        total_retransmissoes += res["retransmissoes"]

    print(f"\nCliente {num} - RTT médio (ms): {(sum/cont * 1000):.3f}")
    print(f"Cliente {num} -  RTT máximo (ms): {(max(rtts) * 1000):.3f}")
    print(f"Cliente {num} -  Tempo total (ms): {(tempo_total * 1000):.3f}")
    print(f"Cliente {num} -  Total de retransmissoes: {total_retransmissoes}")
    print(f"Cliente {num} -  Total de datagramas perdidos: {perdidos}\n")

threads = []

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

tempo_concorrencia = fim_concorrencia - inicio_concorrencia

print(f"Tempo total: {tempo_concorrencia:.3f}s")
