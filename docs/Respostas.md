# Parte 3: Experimento e Análise
Execute o cliente 3 vezes contra o servidor UDP, variando a taxa de perda simulada: 0%, 10%, 30%. Depois, execute uma vez contra o servidor TCP.
Para cada execução, registre:
● Tempo total da sequência completa;
● RTT médio e RTT máximo;
● Número de retransmissões (apenas UDP); e
● Requisições perdidas definitivamente, se houver (esgotou tentativas).

| Caso | Entregues | Perdidos | Retransmissões | RTT Médio (ms) | RTT Máximo (ms) | Duração Total (ms)|
| --- | --- | --- |--- |--- |--- |--- |
| UDP - 0% | 20 | 0 | 0 | 1.049 | 2.077 | 21.107 |
| UDP - 10% | 20 | 0 | 3 | 77.107 | 513.917 | 1542.267 |
| UDP - 30% | 20 | 0 | 11 | 281.973 | 1528.407 | 5639.650 |
| TCP | 20 | 0 | 0 | 0.35 | 0.51 | 7.15 |