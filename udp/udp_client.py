import random
import socket
import time

HOST = "127.0.0.1"
PORT = 6789

operadores = ['+', '-', '*', '/']
resultados = [] #Lista de dicionários

MAX_RETRANSMISSAO = 5 
MAX_TEMPO = 0.5 #Tempo máximo de espera da mensagem em segundos

inicio = time.perf_counter()
ultimo_tempo = inicio

for n in range(20):
    #Cálculo da operação matemática aleatória
    num1 = random.randint(0, 100)
    num2 = random.randint(0, 100)
    op = random.choice(operadores)
    msg = "CALC:" + str(n) + ":" + str(num1) + ":" + op + ":" + str(num2)
    print(msg)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(MAX_TEMPO) 
    recebido = False

    for tentativa in range(1 + MAX_RETRANSMISSAO):
        try:
            s.sendto(bytes(msg, 'utf-8'), (HOST, PORT))
        
            if tentativa != 0:
                print(f"Retransmissão {tentativa} da mensagem {n}")

            data = s.recv(1024).decode('utf-8')
            print(f"{data}")
            agora = time.perf_counter()
            tempo_req = agora - ultimo_tempo
            print(f"n: {n}   tentativa: {tentativa}  tempo_req: {tempo_req}\n")
            #rtt.append(tempo_req)
            resultados.append({
                "rtt": tempo_req,
                "retransmissoes": tentativa
            })
            ultimo_tempo = agora

            recebido = True
            break

        except TimeoutError:
            print(f"Timeout na resposta da mensagem {n}")

    if recebido == False:
        print(F"Nenuma resposta após {MAX_RETRANSMISSAO} retransmissões\n")
        resultados.append({
            "rtt": None,
            "retransmissoes": tentativa
        })
        ultimo_tempo = time.perf_counter()
        

agora = time.perf_counter()
tempo_total = agora - inicio
s.close()


sum = 0
cont = 0
print("Tempo de cada RTT (ms)")
for i in range(20):
    print(f"n: {i}  rtt: {(resultados[i]["rtt"] * 1000):.3f}    retransmissões:{resultados[i]["retransmissoes"]}")

    if resultados[i]["rtt"] != None:
        sum += resultados[i]["rtt"]
        cont += 1

rtts = []
total_retransmissoes = 0
for res in resultados:
    if res["rtt"] is not None:
        rtts.append(res["rtt"])
    total_retransmissoes += res["retransmissoes"]

print(f"\nRTT médio (ms): {(sum/cont * 1000):.3f}")
print(f"RTT máximo (ms): {(max(rtts) * 1000):.3f}")
print(f"Tempo total (ms): {(tempo_total * 1000):.3f}")
print(f"Total de retransmissoes: {total_retransmissoes}\n")