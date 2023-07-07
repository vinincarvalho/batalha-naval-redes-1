# Batalha Naval em Redes
Programação de um socket TCP.

Implementação de um socket TCP para realizar uma batalha naval entre cliente-servidor.

Protocolo da Camada de Aplicação para o Jogo de Batalha Naval:

1. Estabelecimento da Conexão:
   - O cliente inicia a conexão com o servidor através do socket TCP.
   - O cliente envia uma mensagem "StartConnection" para o servidor, contendo o nickname do cliente.
   - O servidor recebe a mensagem, cria uma nova instância de cliente e inicia o jogo.
   - O servidor envia uma mensagem "StartGame" para o cliente, indicando que o jogo começou.

2. Fase de Jogo:
   - Durante a fase de jogo, o cliente e o servidor se alternam realizando ações no jogo.

   - Ações do Cliente:
     - O cliente realiza uma ação de tiro, selecionando uma posição no tabuleiro inimigo.
     - O cliente envia uma mensagem "SHOT x,y" para o servidor, informando as coordenadas do tiro.
     - O servidor recebe a mensagem, verifica se o tiro acertou um navio e responde ao cliente.

   - Ações do Servidor:
     - O servidor recebe a mensagem de tiro do cliente.
     - O servidor realiza uma ação de tiro, selecionando uma posição no tabuleiro do cliente.
     - O servidor envia uma mensagem "HIT x,y" para o cliente, informando que acertou um navio do cliente.
       (ou envia "MISS" se o tiro não acertou nenhum navio)

3. Atualização do Estado:
   - Após cada ação de tiro, o estado do jogo é atualizado e os tabuleiros são exibidos.

   - Cliente:
     - O cliente atualiza seu tabuleiro inimigo com os resultados dos tiros do servidor.
     - O cliente exibe seu tabuleiro e o tabuleiro inimigo.

   - Servidor:
     - O servidor atualiza o tabuleiro do cliente com os resultados dos tiros do cliente.
     - O servidor exibe seu tabuleiro e o tabuleiro do cliente.

4. Finalização do Jogo:
   - O jogo continua até que todas as embarcações de um dos jogadores sejam destruídas.

   - Cliente:
     - Se todas as embarcações do cliente forem destruídas, o cliente recebe a mensagem "END" do servidor,
       indicando que ele venceu o jogo.
     - O cliente exibe a mensagem de vitória e fecha a conexão.

   - Servidor:
     - Se todas as embarcações do servidor forem destruídas, o servidor encerra a conexão com o cliente.
     - O servidor exibe a mensagem de derrota e aguarda por novas conexões.

5. Encerramento da Conexão:
   - Em qualquer momento durante o jogo, se ocorrer um erro ou o cliente encerrar a conexão, o servidor fecha a conexão com o cliente.
   - O servidor exibe a mensagem de desconexão do cliente e continua aguardando por novas conexões.

Mensagens Trocadas:
- Cliente para Servidor:
  - "StartConnection Nick" - Solicita o estabelecimento da conexão com o servidor, fornecendo o apelido do cliente.
  - "SHOT x,y" - Informa ao servidor a posição do tiro realizado pelo cliente.

- Servidor para Cliente:
  - "StartGame" - Indica ao cliente que o jogo começou.
  - "HIT x,y" - Informa ao cliente que o servidor acertou um navio do cliente na posição (x, y).
  - "MISS" - Informa ao cliente que o servidor errou o tiro.
  - "END" - Indica ao cliente que todas as suas embarcações foram destruídas e ele venceu o jogo.

Este protocolo da camada de aplicação define a sequência de eventos, estados e mensagens que as partes comunicantes (cliente e servidor) trocam para manter o software do jogo de Batalha Naval funcionando. Cada parte segue uma lógica específica de acordo com as mensagens recebidas e responde de acordo com as regras do jogo. O protocolo abrange o estabelecimento da conexão, início do jogo, movimentos do cliente e servidor, e o encerramento do jogo.

Funcionamento do Software:

O software implementa o clássico jogo de Batalha Naval, onde dois jogadores competem para afundar os navios do oponente em um tabuleiro 10x10. Cada jogador tem seu próprio tabuleiro e deve posicionar estrategicamente seus navios antes de iniciar a partida. Durante o jogo, os jogadores alternam entre fazer movimentos, selecionando coordenadas para atirar no tabuleiro do oponente, e receber informações sobre o resultado do tiro.

Quando é a vez de um jogador fazer um movimento, ele é solicitado a digitar as coordenadas (linha e coluna) onde deseja atirar. Essas coordenadas são então enviadas para o outro jogador através de uma conexão de rede. O jogo utiliza um protocolo de aplicação personalizado para a troca de mensagens entre o cliente e o servidor.

O servidor é responsável por gerenciar as conexões dos clientes e coordenar as partidas. Ele mantém uma lista de clientes conectados e inicia um novo jogo quando houver pelo menos dois clientes disponíveis. O servidor também é responsável por verificar se um tiro acertou ou errou um navio, atualizar os tabuleiros dos jogadores e determinar quando um jogador venceu o jogo.

O cliente, por sua vez, é responsável por fornecer uma interface de usuário para o jogador. Ele exibe os tabuleiros do jogador e do oponente, bem como as mensagens relevantes durante o jogo, como acertos, erros e mensagens de vitória ou derrota. O cliente também é responsável por enviar as coordenadas de tiro escolhidas pelo jogador para o servidor e receber as mensagens do servidor com o resultado do tiro.

Propósito do Software:

O propósito do software é fornecer uma experiência interativa e divertida do jogo de Batalha Naval para dois jogadores. O software permite que os jogadores se conectem entre si por meio de uma rede, competindo em partidas emocionantes e estratégicas. O objetivo é afundar todos os navios do oponente enquanto protege os próprios navios. O software oferece uma maneira conveniente e envolvente de jogar Batalha Naval, eliminando a necessidade de tabuleiros físicos e peças.

Motivação da Escolha do Protocolo de Transporte:

O protocolo de transporte escolhido para a implementação do jogo de Batalha Naval é o TCP (Transmission Control Protocol). O TCP foi selecionado devido às suas características de confiabilidade e controle de fluxo. No contexto do jogo de Batalha Naval, é essencial que as mensagens trocadas entre o cliente e o servidor cheguem corretamente e na ordem correta. A confiabilidade do TCP garante que não haja perda de dados durante a transmissão e que as mensagens sejam entregues sem erros. Além disso, o TCP possui mecanismos de controle de fluxo que garantem que a comunicação entre as partes seja ajustada para evitar congestionamento de rede.

Requisitos Mínimos de Funcionamento:

Para que o software do jogo de Batalha Naval funcione corretamente, são necessários alguns requisitos mínimos:

- Conexão de rede TCP/IP: O software requer uma conexão de rede TCP/IP para estabelecer a comunicação entre o cliente e o servidor.

- Servidor em execução: O servidor deve estar em execução e aguardando conexões dos clientes. Ele deve ser capaz de lidar com múltiplas conexões simultâneas de clientes.

- Estabelecimento de conexão: O cliente deve fornecer um nickname ao estabelecer a conexão com o servidor. Isso permite que o servidor identifique os jogadores.

- Inicialização dos tabuleiros: Os tabuleiros de ambos os jogadores devem ser corretamente inicializados antes do início da partida. Os navios devem ser posicionados estrategicamente no tabuleiro de cada jogador.

- Troca de mensagens: O software deve garantir que as mensagens sejam enviadas e recebidas corretamente entre o cliente e o servidor. Isso envolve a implementação de um protocolo de aplicação personalizado para definir a estrutura e o formato das mensagens trocadas.

- Atualização dos tabuleiros: Após cada tiro realizado, os tabuleiros dos jogadores devem ser atualizados para refletir o resultado do tiro. Os acertos devem ser marcados no tabuleiro do oponente, enquanto as falhas devem ser marcadas no próprio tabuleiro.

- Tratamento de vitória ou derrota: O software deve ser capaz de detectar quando um jogador afundou todos os navios do oponente. Nesse caso, o jogo deve ser encerrado adequadamente, exibindo uma mensagem de vitória para o jogador vencedor e encerrando a conexão entre o cliente e o servidor.

- Tratamento de desconexão: O software deve ser capaz de lidar com a desconexão de um cliente durante uma partida. Se um jogador desconectar, o jogo deve ser interrompido de forma adequada, exibindo uma mensagem informando a desconexão e encerrando a conexão com o cliente remanescente.

Esses requisitos mínimos garantem que o software do jogo de Batalha Naval funcione corretamente, permitindo aos jogadores estabelecer conexões, jogar partidas completas e obter uma experiência de jogo satisfatória. A escolha do TCP como protocolo de transporte, juntamente com a implementação adequada do protocolo de aplicação, garante uma comunicação confiável entre o cliente e o servidor, essencial para o correto funcionamento do jogo.
