# Atividade de comunicação com sockets
Sistemas Distribuídos e Redes de Comunicação  
Maria Carolina - 603274

## Sobre
O projeto implementa o serviço cliente-servidor duas vezes, uma sobre UDP e outra sobre TCP.   
O objetivo é demonstrar, de forma prática, o funcionamento da comunicação cliente-servidor utilizando sockets em Python e comparar empiricamente o comportamento dos dois protocolos.

## Tecnologias utilizadas
- Python 3
- Biblioteca padrão `socket`
- Protocol Buffers
- `protoc` - Compilador do Protocol Buffers

Não é necessário instalar bibliotecas ou dependências externas para executar o projeto.

## Estrutura do projeto
```
.
├── docs
│ └── Respostas.md
│ 
├── protobuf/           # Implementação do TCP com serialização usando Protocol Buffers (Parte 4)
│ ├── calc_pb2.py
│ ├── calc.proto 
│ ├── proto_client.py   # CalcClientProto 
│ └── proto_server.py   # CalcServerProto  
│ 
├── tcp/                # Parte 2
│ ├── tcp_client.py     # CalcClientTCP
│ └── tcp_server.py     # CalcServerTCP
│ 
├── udp/                # Parte 1
│ ├── udp_client.py     # CalcClientUDP (com timeout e retransmissão)
│ └── udp_server.py     # CalcServerUDP (com simulação de perda configurável) 
│ 
└── README.md

```

## Como executar
### TCP

Primeiramente, execute o servidor:

```bash
python tcp/tcp_server.py
```

Em outro terminal, execute o cliente:

```bash
python tcp/tcp_client.py
```

O cliente estabelecerá uma conexão com o servidor e poderá realizar a troca de mensagens utilizando o protocolo TCP.  
O cliente gera mensagens aleatórias com operações matemáticas simples, o servidor resolve a conta e o cliente exibe o resultado.

### UDP
Em um terminal, execute o servidor. O parâmetro `--loss-rate` define a porcentagem de datagramas que serão perdidos e aceita valores de `0.0` a `1.0`. 

```bash
python udp/udp_server.py --loss-rate 0.1
```

Caso não seja passado nenhum valor, o servidor executará `--loss-rate` com valor `0.1`.

Em outro terminal, execute o cliente:

```bash
python udp/udp_client.py
```

## Protocol Buffers usando o TCP
Primeiramente, execute o servidor:

```bash
python protobuf/proto_server.py
```

Em outro terminal, execute o cliente:

```bash
python protobuf/proto_client.py
```
