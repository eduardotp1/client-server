# Projeto 2 : Datagrama

## Datagrama

Datagrama é um processo de empacotamento dos dados a serem transmitidos numa comunicação ponto a ponto, para serem detectadas falhas caso ocorram durante a transmissão e/ou recebimento de um dado. É o oposto de streaming de dados.

Quando, em um streaming de dados, um byte é perdido, o receptor ao pegar os dados, pode acabar misturando de forma equivocada bytes do próximo pacote, no pacote atual, já que este possui um byte a menos. Isso faz com que os dados sejam recebidos errados, e sem um mecanismo de detecção dessas falhas, a comunicação/envio dos dados precisaria ser reiniciado muito tempo depois.

![Errodecomunicacao](doc/erro.png){ width=100% }

Para detectar esse tipo de falha, cria-se um "pacote" com o dado que se deseja enviar, onde há bytes de controle que informam qual o início do pacote, ao tamanho desse pacote, e o fim do mesmo. Assim, ao receber um pacote, o receptor pode conferir se ele começa e termina como deveria, e se esse pacote tem o tamanho que deveria ter. Dessa forma, ambos os pontos tem mais confiança de que o dado recebido é o mesmo que o enviado.

## Implementação

Para essa implementação, foi adicionado um 'HEAD' (cabeçalho) no começo dos dados que se quer enviar (payload). Esse HEAD é composte de um ou mais bytes de início de pacote e o tamanho que esse pacote possui. Ao final desse pacote que já contém Head e payload, é adicionado um EOP (End of packet, ou fim de pacote) para informar que esses são os bytes finais do pacote.

![Datagrama](doc/datagrama.png){ width=100% }

## Comunicação

Uma função chamada Empacota realiza o processo de criar o pacote, adicionando os bytes do HEAD, logo após os dados do que se deseja enviar e por fim o EOP.
Esse pacote é enviado ao receptor e, após ser recebido, para ele ser desempacotado, primeiro uma função chamada HeadPayload encontra o EOP do primeiro pacote no Buffer e o retira, salvando apenas os fragmentos Head + payload em uma variável e atualizando o buffer, já que o primeiro pacote presente nele já foi recuperado. Outra função retira o Head da variável e assim, tem acesso aos dados sozinhos, tendo assim recuperado os dados que se desejava enviar.


