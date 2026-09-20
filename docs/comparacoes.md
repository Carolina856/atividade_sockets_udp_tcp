# Comparações entre as implementações
## Parte 3: Experimento e Análise
Execute o cliente 3 vezes contra o servidor UDP, variando a taxa de perda simulada: 0%, 10%, 30%. Depois, execute uma vez contra o servidor TCP.
Para cada execução, registre:
- Tempo total da sequência completa;
- RTT médio e RTT máximo;
- Número de retransmissões (apenas UDP); e
- Requisições perdidas definitivamente, se houver (esgotou tentativas).

| Caso | Entregues | Perdidos | Retransmissões | RTT Médio (ms) | RTT Máximo (ms) | Duração Total (ms)|
| --- | --- | --- |--- |--- |--- |--- |
| UDP - 0% | 20 | 0 | 0 | 0.598 | 0.989 | 18.032 |
| UDP - 10% | 20 | 0 | 3 | 77.381 | 514.296 | 1553.708 |
| UDP - 30% | 20 | 0 | 10 | 256.561 | 1029.637 | 5138.448 |
| TCP | 20 | 0 | 0 | 0.323 | 1.614 | 12.771 |


## Parte 4: Implementação com Protocol Buffers
O comportamento deve ser equivalente ao da Parte 2 (TCP, N=20 requisições, mede RTT),
mas com as mensagens serializadas em binário pelo protobuf.

Meça e registre o tamanho médio das mensagens (em bytes) e compare com o
protocolo textual da Parte 2.

| Caso | Tamanho Médio | RTT Médio (ms) | RTT Máximo (ms) | Duração Total (ms) |
| --- | --- | --- |--- |--- |
| TCP Textual | 14.400 | 0.268 | 0.865 | 11.432 |
| TCP com Protocol Buffers | 8.9 | 0.414 | 2.440 | 12.519 |