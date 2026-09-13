import socket
import operator

def calc_result(received_msg):
    operadores = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
    }

    msg = received_msg.split(":")
    num1 = int(msg[2])
    op_string = msg[3]
    num2 = int(msg[4])

    if op_string in operadores:
        try:
            result = operadores[op_string](num1, num2) 
            return "RESULT:" + msg[1] + ":" + str(result)
        except ZeroDivisionError:
            return "ERROR:" + msg[1] + ":Divisão por zero"
    else:
        return "ERROR:" + msg[1] + ":Aconteceu um erro"
        

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 6789))
s.listen(1)
print(f"Servidor rodando")

while True:
    conn, addr = s.accept()
    print(f"Conectado com {addr}")

    while True:
        data = conn.recv(1024)
        if not data:
            break

        msg = data.decode('utf-8')
        print(f"Mensagem recebida: {msg}")
        final_data = str(calc_result(msg))
        conn.sendall(bytes(final_data, 'utf-8'))

    print(f"Finalizando conexão com {addr}")
    conn.close()