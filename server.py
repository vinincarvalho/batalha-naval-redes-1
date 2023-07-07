import socket
import _thread
from time import strftime
from game import TabuleiroServidor as Tabuleiro
import game

# Dados para estabelecer a conexão
HOST = 'localhost'
PORT = 12345

clientesConectados = []
tabuleiro = None

# Cria um socket para estabelecer a conexão
# AF_INET indica que a conexão será baseada no protocolo IPv4
# SOCK_STREAM indica que a conexão será estabelecida utilizando o protocolo TCP
socketConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# Pega o horário do servidor
def getTime():
    return strftime("%d/%m/%Y %H:%M:%S")

# Essa classe define um cliente do servidor
class Cliente:
    def __init__(self, nome, conexao, clientaddress):
        self.nome = nome
        self.conexao = conexao
        self.cliente = clientaddress

    def getNomeCliente(self):
        return self.nome

    def getConexaoCliente(self):
        return self.conexao

    def getCliente(self):
        return self.cliente

# Começa a partida entre cliente e o servidor
def startGame(client):
    clientName = client.getNomeCliente()
    conexaoCliente = client.getConexaoCliente()
    
    print('{}: Server conectado por {}'.format(getTime(), clientName))

    # Envia a mensagem que o jogo começou
    conexaoCliente.sendall('StartGame'.encode('utf-8'))
    print("O Jogo Começou!")

    while True:
        try:
            # Recebe mensagem do cliente
            mensagem = conexaoCliente.recv(1024)
            mensagem = mensagem.decode('utf-8')

            # Caso não venha nada, finaliza a conexão
            if not mensagem:
                print('{}: Cliente {} finalizou a conexão.'.format(getTime(), clientName))
                clientesConectados.remove(client)
                for p in clientesConectados:
                    p.getConexaoCliente().sendall('Cliente {} desconectou-se!'.format(clientName).encode('utf-8'))
                break

            # Mostra a mensagem recebida
            print('{}: Cliente {} enviou -> {}'.format(getTime(), clientName, mensagem))

            # Se a mensagem for igual a "SHOT", o servidor recebe o tiro
            if "SHOT" in mensagem:
                params = mensagem.replace('SHOT ', '').split(',')
                x = int(params[0])
                y = int(params[1])
                # Verifica se o cliente acertou o tiro
                if str(tabuleiro.get(x, y)) != ' ' and str(tabuleiro.get(x, y)) != 'X':
                    tabuleiro.set(x, y, 'X')
                    print("{} acertou o tiro na posição {}, {}".format(clientName,x, y))
                    print("Rodada do Cliente, novamente!")
                    print(tabuleiro.campo)
                    # Verifica se ainda existe algum navio no tabuleiro, caso não o jogo é finalizado
                    if (tabuleiro.quantidade_a == 0 and tabuleiro.quantidade_n == 0 and tabuleiro.quantidade_c == 0 and tabuleiro.quantidade_s == 0 ):
                        conexaoCliente.sendall("END".encode('utf-8'))
                        break
                    # Imprime a quantidade de navios restantes
                    print( str(tabuleiro.quantidade_a) + " "  + str(tabuleiro.quantidade_n) + " " + str(tabuleiro.quantidade_c) + " "  + str(tabuleiro.quantidade_s) )
                    conexaoCliente.sendall("HIT {},{}".format(x, y).encode('utf-8'))
                # Caso o cliente tenha errado o tiro
                else:
                    print("{} errou o tiro na posição {}, {}".format(clientName,x, y))
                    print("Rodada do Servidor!")
                    conexaoCliente.sendall("MISS".encode('utf-8'))
                    game.shot(conexaoCliente)

            # Se a mensagem for igual a "HIT", o servidor acertou o alvo
            if "HIT" in mensagem:
                print("Você acertou! Sua vez novamente!")
                params = mensagem.replace('HIT ', '').split(',')
                x = int(params[0])
                y = int(params[1])
                tabuleiro.setEnemy(x, y, 'X')
                print("Voce: ")
                print(tabuleiro.campo)
                print("Inimigo: ")
                print(tabuleiro.campo_inimigo)
                game.shot(conexaoCliente)

            # Se a mensagem for igual a "MISS", o servidor errou o alvo e a vez passa para o cliente
            if "MISS" in mensagem:
                print("Você errou, rodada do oponente!")
                print(tabuleiro.campo) # Mostra o estado do campo de batalha
        
        # Ocorreu algum erro
        except Exception as e:
            print('{}: Ocorreu um erro na conexão com o cliente {}.'.format(getTime(), clientName))
            print('Erro : ' + str(e))
            clientesConectados.remove(client)
            for p in clientesConectados:
                p.getConexaoCliente().sendall('Cliente {} desconectou-se!'.format(clientName).encode('utf-8'))
            break

    print('Finalizando conexão com', clientName)
    conexaoCliente.close()
    _thread.exit()

socketConnection.bind((HOST, PORT))        # Associar o socket s com a rede especificada 
socketConnection.listen(1)                 # Abilita o servidor a receber 1 conexao por vez

# Sempre que o servidor receber uma nova conexao cria uma thread para o cliente que se conectou:
def startConnection():
    while True:
        print("Aguardando conexão...")
        conn, cliente = socketConnection.accept()   # .accept() retorna um novo objeto do tipo socket e o endereco do cliente (host:port)
        msg = conn.recv(1024).decode('utf-8') # .recv() recebe a mensagem enviada pelo cliente na conexao (con)
        print('Connected by', cliente)
        print("MensagemRecebida = " + msg)
        if 'StartConnection' in msg:

            # Inicializa e exibe o tabuleiro do servidor
            global tabuleiro 
            tabuleiro = Tabuleiro()
            print(tabuleiro.campo)
                
            #Criar novo cliente com o socket da conexao ativa
            clienteNovo = Cliente(msg.split(' ', 1)[1], conn, cliente)
            clientesConectados.append(clienteNovo)
            for x in clientesConectados:
                x.getConexaoCliente().sendall('Cliente {} conectado!'.format(clienteNovo.getNomeCliente()).encode('utf-8'))
            _thread.start_new_thread(startGame, tuple([clienteNovo]))
        else:
            print('Cliente {} desatualizado!'.format(cliente[1]))
            conn.sendall('Seu cliente está desatualizado! Favor atualizar e tentar novamente!'.encode('utf-8'))
            conn.close()
            print('Conexão com cliente {} finalizada'.format(cliente[1]))

startConnection()

# o novo socket recebido pelo accept é o que usaremos para comunicar com o cliente, é diferente do socket que escuta para receber novas conexões 
# o loop infinito le qualquer dado que o cliente envia e responde com .sendall()
# se conn.recv() retorna um objeto byte vazio, o cliente fecha a conexao e o loop infinito termina,
# with conn "metodo" automaticamente fecha o socket no final do bloco
# .accept() # return new socket object and a tuple with address of client (host port)