import random
import numpy as np

# Classe que define o tabuleiro do cliente (é uma matriz)
class TabuleiroCliente:
    
    campo = None
    campo_inimigo = None
    quantidade_a = None
    quantidade_n = None
    quantidade_c = None
    quantidade_s = None
    
    def __init__(self):
        self.campo = np.zeros(shape=(10,10), dtype=int) # Cria uma matriz 10x10 com 0 em tudo
        self.campo = self.campo.astype(str) # Mudar tipo int para string
        self.campo[self.campo == '0'] = ' ' # Trocar 0 por espaco em branco
        self.quantidade_a = 0
        self.quantidade_n = 0
        self.quantidade_c = 0
        self.quantidade_s = 0
        self.setShipsPositions() # Carregar posicoes do arquivo
        self.setEnemyField()
        
    def setEnemyField(self):
        self.campo_inimigo = np.zeros(shape=(10,10), dtype=int) # Cria uma matriz 10x10 com 0 em tudo
        self.campo_inimigo = self.campo_inimigo.astype(str) # Mudar tipo int para string
        self.campo_inimigo[self.campo_inimigo == '0'] = ' ' # Trocar 0 por espaco em branco
    
    #Get position value
    def get(self, x, y):
        return self.campo[x][y]
    
    #Set position value
    def set(self, x, y, valor):
        if valor == 'X':
            if self.campo[x][y] == 'A':
                self.quantidade_a -= 1
            elif self.campo[x][y] == 'N':
                self.quantidade_n -= 1
            elif self.campo[x][y] == 'C':
                self.quantidade_c -= 1
            elif self.campo[x][y] == 'S':
                self.quantidade_s -= 1
        self.campo[x][y] = valor
        
    #Set position value
    def setEnemy(self, x, y, valor):
        self.campo_inimigo[x][y] = valor
    
    #Inserir Porta Aviao
    def insertAircraftCarrier(self, x, y, horizontalOrVertical):
        self.set(x, y, 'A')
        self.quantidade_a += 5
        if horizontalOrVertical == 0:
            self.set(x, y + 1, 'A')
            self.set(x, y + 2, 'A')
            self.set(x, y + 3, 'A')
            self.set(x, y + 4, 'A')
        else:
            self.set(x + 1, y, 'A')
            self.set(x + 2, y, 'A')
            self.set(x + 3, y, 'A')
            self.set(x + 4, y, 'A')
    
    #Inserir Navio Tanque
    def insertTankShip(self, x, y, horizontalOrVertical):
        self.set(x, y, 'N')
        self.quantidade_n += 4
        if horizontalOrVertical == 0:
            self.set(x, y + 1, 'N')
            self.set(x, y + 2, 'N')
            self.set(x, y + 3, 'N')
        else:
            self.set(x + 1, y, 'N')
            self.set(x + 2, y, 'N')
            self.set(x + 3, y, 'N')

    #Inserir ContraTorpedeiro
    def insertDestroyer(self, x, y, horizontalOrVertical):
        self.set(x, y, 'C')
        self.quantidade_c += 3
        if horizontalOrVertical == 0:
            self.set(x, y + 1, 'C')
            self.set(x, y + 2, 'C')
        else:
            self.set(x + 1, y, 'C')
            self.set(x + 2, y, 'C')
    
    #Inserir Submarino
    def insertSub(self, x, y, horizontalOrVertical):
        self.set(x, y, 'S')
        self.quantidade_s += 2
        if horizontalOrVertical == 0:
            self.set(x, y + 1, 'S')
        else:
            self.set(x + 1, y, 'S')
    
    # Definir posicoes do cliente com base no arquivo denonimado coordenadas.txt
    def setShipsPositions(self): 
        arquivo = open("coordenadas.txt", "r")
        for x in arquivo:
            fileLine = x.replace("\n", "") # Ler linha do arquivo, removendo terminacao de linha
            line = fileLine.split(" ") # Separar a linha do arquivo por espaco
            linha = int(line[0]) # Linha do tabuleiro definida pela linha lida do arquivo
            coluna = int(line[1]) # Coluna do tabuleiro definida pela linha lida do arquivo
            horizontalOrVertical = int(line[2]) # Posicao horizontal(0) ou vertical(1) do tabuleiro definida pela linha lida do arquivo
            navio = line[3] # Tipo de navio definido no arquivo
            if navio == 'A': # A = Porta Avioes
                self.insertAircraftCarrier(linha, coluna, horizontalOrVertical)
            elif navio == 'N': # Navio Tanque
                self.insertTankShip(linha, coluna, horizontalOrVertical)
            elif navio == 'C': # Contra Torpedeiros
                self.insertDestroyer(linha, coluna, horizontalOrVertical)
            elif navio == 'S': # Submarino
                self.insertSub(linha, coluna, horizontalOrVertical)
        arquivo.close()

class TabuleiroServidor:
    
    campo = None
    campo_inimigo = None
    quantidade_a = None
    quantidade_n = None
    quantidade_c = None
    quantidade_s = None
    
    def __init__(self):
        self.campo = np.zeros(shape=(10,10), dtype=int) # Cria uma matriz 10x10 com 0 em tudo
        self.campo = self.campo.astype(str) # Mudar tipo int para string
        self.campo[self.campo == '0'] = ' ' # Trocar 0 por espaco em branco
        self.quantidade_a = 0
        self.quantidade_n = 0
        self.quantidade_c = 0
        self.quantidade_s = 0
        self.setShipsPositions()
        self.setEnemyField()
    
    def setEnemyField(self):
        self.campo_inimigo = np.zeros(shape=(10,10), dtype=int) # Cria uma matriz 10x10 com 0 em tudo
        self.campo_inimigo = self.campo_inimigo.astype(str) # Mudar tipo int para string
        self.campo_inimigo[self.campo_inimigo == '0'] = ' ' # Trocar 0 por espaco em branco

    #Get position value
    def get(self, x, y):
        return self.campo[x][y]
    
    #Set position value
    def set(self, x, y, valor):
        if valor == 'X':
            if self.campo[x][y] == 'A':
                self.quantidade_a -= 1
            elif self.campo[x][y] == 'N':
                self.quantidade_n -= 1
            elif self.campo[x][y] == 'C':
                self.quantidade_c -= 1
            elif self.campo[x][y] == 'S':
                self.quantidade_s -= 1
        self.campo[x][y] = valor
    
    #Set position value
    def setEnemy(self, x, y, valor):
        self.campo_inimigo[x][y] = valor

    #Inserir Porta Aviao
    def insertAircraftCarrier(self, x, y, horizontalOrVertical):
        self.set(x, y, 'A')
        self.quantidade_a += 5
        if horizontalOrVertical == 0:
            self.set(x, y + 1, 'A')
            self.set(x, y + 2, 'A')
            self.set(x, y + 3, 'A')
            self.set(x, y + 4, 'A')
        else:
            self.set(x + 1, y, 'A')
            self.set(x + 2, y, 'A')
            self.set(x + 3, y, 'A')
            self.set(x + 4, y, 'A')
    
    #Inserir Navio Tanque
    def insertTankShip(self, x, y, horizontalOrVertical):
        self.set(x, y, 'N')
        self.quantidade_n += 4
        if horizontalOrVertical == 0:
            self.set(x, y + 1, 'N')
            self.set(x, y + 2, 'N')
            self.set(x, y + 3, 'N')
        else:
            self.set(x + 1, y, 'N')
            self.set(x + 2, y, 'N')
            self.set(x + 3, y, 'N')

    #Inserir ContraTorpedeiro
    def insertDestroyer(self, x, y, horizontalOrVertical):
        self.set(x, y, 'C')
        self.quantidade_c += 3
        if horizontalOrVertical == 0:
            self.set(x, y + 1, 'C')
            self.set(x, y + 2, 'C')
        else:
            self.set(x + 1, y, 'C')
            self.set(x + 2, y, 'C')
    
    #Inserir Submarino
    def insertSub(self, x, y, horizontalOrVertical):
        self.set(x, y, 'S')
        self.quantidade_s += 2
        if horizontalOrVertical == 0:
            self.set(x, y + 1, 'S')
        else:
            self.set(x + 1, y, 'S')
    
    #Checar se posicao gerada é valida
    def checkPosition(self, cord_x, y, horizontalOrVertical, numPos):
        isPositionValid = True
        if horizontalOrVertical == 0:
            for x in range(y, y + numPos, 1):
                if self.get(cord_x, x) != ' ':
                    isPositionValid = False
            return isPositionValid
        else:
            for x in range(cord_x, cord_x + numPos, 1):
                if self.get(x, y) != ' ':
                    isPositionValid = False
            return isPositionValid
    
    #Gerar uma posicao(x,y,orientacao) aleatoria
    def pickPos(self, x):
        linha = random.randint(0, 9)
        coluna = random.randint(0, 9)
        horizontalOrVertical = random.randint(0, 1)
        if horizontalOrVertical == 0:
            while (coluna + x) > 9:
                coluna = random.randint(0, 10)
        else:
            while (linha + x) > 9:
                linha = random.randint(0, 10)
        return linha, coluna, horizontalOrVertical
    
    # Definir posicoes do tabuleiro do servidor aleatoriamente
    def setShipsPositions(self):
        shipNumbers = 1
        for x in range(4, 0, -1):
            for y in range(1, shipNumbers + 1, 1):
                linha, coluna, horizontalOrVertical = self.pickPos(x)
                while not self.checkPosition(linha, coluna, horizontalOrVertical, x + 1):
                    linha, coluna, horizontalOrVertical = self.pickPos(x)
                if x == 1:
                    self.insertSub(linha, coluna, horizontalOrVertical)
                elif x == 2:
                    self.insertDestroyer(linha, coluna, horizontalOrVertical)
                elif x == 3:
                    self.insertTankShip(linha, coluna, horizontalOrVertical)
                elif x == 4:
                    self.insertAircraftCarrier(linha, coluna, horizontalOrVertical)
            shipNumbers = shipNumbers + 1

def shot(conexao):
    print("Exemplo de entrada: 0,2 onde 0 = linha (x) e 2 = coluna (y)")
    teclado = str(input("Digite onde deseja atirar: ").replace(".", ","))
    local = teclado.split(',')
    linha = int(local[0])
    coluna = int(local[1])
    while (linha > 9 or linha < 0) or (coluna > 9 or coluna < 0):
        print("Entrada inválida! Tente outra vez, por favor.")
        local = str(input("Digite onde deseja atirar: ")).split(',')
        linha = int(local[0])
        coluna = int(local[1])
    print("Atirando na posição {}, {}...".format(linha, coluna))
    conexao.sendall("SHOT {},{}".format(linha, coluna).encode('utf-8'))