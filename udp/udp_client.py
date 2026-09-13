import random
import socket
import time

HOST = "127.0.0.1"
PORT = 6789

operadores = ['+', '-', '*', '/']
rtt = []

MAX_TENTATIVAS = 6 #1 envio + 5 retransmissões
MAX_TEMPO = 0.5 #Tempo de espera da mensagem

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

    for tentativa in range(MAX_TENTATIVAS):
        try:
            inicio = time.perf_counter()
            s.sendto(bytes(msg, 'utf-8'), (HOST, PORT))

            if tentativa == 0:
                print(f"Mensagem {n} enviada!")
            else:
                print(f"Retransmissão {tentativa} da mensagem {n}")

            data = s.recv(1024).decode('utf-8')
            print(f"{repr(data)}\n")
            fim = time.perf_counter()
            tempo = fim - inicio
            rtt.append(tempo)
            recebido = True
            break

        except TimeoutError:
            print(f"Timeout na resposta da mensagem {n}")

    if recebido == False:
        print("Nenuma resposta após 5 retransmissões\n")
        rtt.append(0) #Zero significa que o cliente não recebeu a resposta

s.close()

print("Tempo de cada RTT")
for i in range(20):
    print(f"{i}: {rtt[i]}")