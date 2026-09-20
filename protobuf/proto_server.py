import socket
import operator
import calc_pb2
import threading

def calc_result_proto(received_msg):
    operadores = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
        }

    res = calc_pb2.CalcResult()
    res.n_seq = received_msg.n_seq
    
    if received_msg.op in operadores:
        try:
            res.result = operadores[received_msg.op](received_msg.operando1, received_msg.operando2)
            res.status = "RESULT"
            return res

        except ZeroDivisionError:
            return res
    else:
        return res

def clients(conn, addr):
    print(f"Conectado com {addr}")

    while True:
        data = conn.recv(1024)

        if not data:
            break    

        msg = calc_pb2.CalcRequest()
        msg.ParseFromString(data)
        print(f"CALC:{msg.n_seq}:{msg.operando1}:{msg.op}:{msg.operando2}\n")

        final_data = calc_result_proto(msg)
        conn.sendall(final_data.SerializeToString())    

    print(f"Finalizando conexão com {addr}")
    conn.close()   

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 6789))
s.listen(5)
print(f"Servidor rodando")

while True:
    conn, addr = s.accept()

    thread = threading.Thread(
        target=clients,
        args=(conn, addr)
    )
    thread.start()       