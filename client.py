import socket
import ipaddress
from game import TabuleiroCliente as Tabuleiro
import game

def testar_ip(ip):
    try:
        ip = ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

#Dados para conexao
HOST = 'localhost'
PORT = 12345
Nick = 'CLIENTE'

socketConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET = IPV4, SOCK_STREAM = TCP

socketConnection.connect((HOST, PORT)) # Estabelecer conexao e iniciar handshake de tres vias

tabuleiro = Tabuleiro() # Inicializar o tabuleiro do cliente
print (tabuleiro.campo) # Imprimir na tela o tabuleiro do cliente

mensagem = 'StartConnection ' + Nick # Enviar para o servidor informacao para estabelecer conexao
socketConnection.sendall(mensagem.encode('utf-8'))
print("Enviado -> " + mensagem)

while True:
    try:
        data = socketConnection.recv(1024) # Recebe dados do servidor, se vazio fecha a conexao / 1024 = quantidade maxima de dados por vez
        if data:
            mensagemRecebida = data.decode('utf-8')
            if 'StartGame' in mensagemRecebida:
                print("O Jogo Começou!")
                print("Sua vez de atirar!")
                game.shot(socketConnection)
            if 'HIT' in mensagemRecebida:
                print('---')
                print("Você acertou! Sua vez novamente!")
                params = mensagemRecebida.replace('HIT ', '').split(',')
                x = int(params[0])
                y = int(params[1])
                tabuleiro.setEnemy(x,y,'X')
                print("Voce: ")
                print(tabuleiro.campo)
                print("Inimigo: ")
                print(tabuleiro.campo_inimigo)
                game.shot(socketConnection)
            if 'MISS' in mensagemRecebida:
                print('---')
                print("Você errou, rodada do oponente!")
            if 'SHOT' in mensagemRecebida:
                print('---')
                params = mensagemRecebida.replace('SHOT ', '').split(',')
                x = int(params[0])
                y = int(params[1])
                if str(tabuleiro.get(x, y)) != ' ' and str(tabuleiro.get(x, y)) != 'X':
                    tabuleiro.set(x, y, 'X')
                    print("O Servidor acertou o tiro na posição {}, {}".format(x, y))
                    print("Rodada do servidor, novamente!")
                    print(tabuleiro.campo)
                    socketConnection.sendall("HIT {},{}".format(x, y).encode('utf-8')) # Envia dados para o servidor informando que ele acertou um navio do cliente
                else:
                    print("Servidor errou o tiro na posicao {}, {}".format(x, y))
                    print('---')
                    print("Sua vez!")
                    socketConnection.sendall("MISS".encode('utf-8')) # Envia dados para o servidor informando que NAO acertou nenhum navio do cliente
                    game.shot(socketConnection)
            if 'END' in mensagemRecebida:
                print("Voce venceu!!")
                print('Closing connection')
                socketConnection.close()
                break
    except:
        print('Closing connection')
        socketConnection.close()
        break