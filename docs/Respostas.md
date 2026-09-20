# Respostas

## Parte 1 - UDP
*Dados das execuções UDP — grade com linhas 0%, 10%, 30% e colunas: Tempo total (s) · RTT médio (ms) · Retransmissões · Perdidas definitivamente*

0%: 0,018s - 0,598ms - 0 - 0

10%: 1,553s - 77,381ms - 3 - 0

30%: 5,138s - 256,561ms - 10 - 0

*Descreva como você implementou o timeout + retransmissão no cliente UDP. O que acontece quando o número máximo de tentativas é esgotado? O cliente consegue detectar sozinho que uma requisição foi perdida?*

Eu defini o número máximo de retransmissões e o tempo máximo de espera da resposta como constantes. Para cada requisição, eu tento enviar um cálculo. Se o resultado não a tempo, o cliente dá TimeOutError e envia o cálculo novamente até esgotar o número de tentativas. Se as tentativas forem esgotadas, o RTT daquela requisição é salvo como None e o número de retransmissões é salvo como o número máximo de retransmissões. 

## Parte 2 - TCP
*Dados da execução TCP: Tempo total (s) e RTT médio (ms)*

12,771s - 0,323ms


*Como o servidor TCP trata múltiplos clientes?*

Thread por cliente

*Por que o cliente TCP não precisou de timeout ou retransmissão, enquanto o cliente UDP precisou? Compare os tempos e RTTs das duas implementações com perda 0%.*

O UDP é um protocolo sem conexão que não garante a entrega dos datagramas. Se um datagrama for perdido, o servidor não envia automaticamente uma nova cópia, por isso foi necessário implementar um mecanismo de timeout e de retransmissão no cliente servidor. Já o TCP garante a entrega confiável e ordenada dos dados. 
Com relação ao tempo, percebe-se que o UDP 0% teve o tempo parecido com o do TCP, embora um pouco maior. Por outro lado, o tempo do UDP 0% foi bem menor do que o 10% e 30% porque não foi necessário esperar o timeout nem retransmitir nenhum datagrama.

## Parte 3 - Análise
*O que acontece com as requisições quando o cliente UDP roda sem retransmissão? Com ela ativada, o que muda — e a que custo em tempo? Apoie com os dados coletados.*

Quando o cliente UDP roda sem retransmissão, não há garantia de que ele receberá todos os datagramas. Como o código tem timeout, o cliente não ficaria esperando um datagrama que não chegaria. Ao adicionar a retransmissão, o tempo aumenta no geral, mas há a garantia de que o cliente tentará obter o pacote novamente (desde que a retransmissão esteja dentro do limite definido). 

UDP 10%: 3 retransmissões - 0 perdidos - 1,533s no total

UDP 30%: 10 retransmissões - 0 perdidos - 5,138s no total

*Dado que UDP exige todo esse trabalho extra para ser confiável, por que ele ainda é usado em sistemas reais? Cite pelo menos um exemplo concreto e justifique.* 

Ele é utilizado em sistemas cujo principal objetivo é reduzir a latência e não garantir a entrega de todas as informações. Nesses sistemas, perder alguns pacotes pode ser menos prejudicial do que esperar por sua retransmissão.

Exemplo: chamada de voz ou vídeo. Se um pacote contendo um pequeno trecho de áudio ou vídeo for perdido, retransmiti-lo pode fazer com que ele chegue atrasado, o que pode resultar em travamentos ou aumento do atraso da comunicação.

## Parte 4 - Protobuf
*Comparar tamanho médio das mensagens. Texto puro em bytes (parte 2) x Protobuf em bytes (parte 4):*

Texto puro em bytes: 14,400

Protobuf em bytes: 8,9

*Como você mediu o tamanho das mensagens?*

Eu transformei as mensagens em bytes e usei a função len() nelas

*Em qual cenário real você escolheria protobuf em vez de texto simples? Foi mais fácil ou mais difícil de implementar? E por quê?*

Protobuf é melhor quando a comunicação entre sistemas envolve muitas mensagens estruturadas, especialmente quando eficiência e padronização são importantes. 
No projeto, foi mais difícil implementar com protobuf do que com texto simples. Com texto simples, eu montei uma string e a converti em bytes. No tcp_server, foi só separar a mensagem usando split(":").
Já no protobuf, foi preciso criar o arquivo .proto, gerar o código python com protoc e atualizar o código do TCP para utilizar o arquivo calc_pb2.py. Sem contar o tempo gasto para instalar o protoc e aprender a usá-lo.