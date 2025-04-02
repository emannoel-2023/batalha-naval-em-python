from abc import ABC, abstractmethod
import random

class Posicao:
    """posicao no tabuleiro do jogo."""
    
    def __init__(self, linha, coluna):
        """
        Inicia uma posicao com linha e coluna.
        
        Args:
            linha (int): Coordenada da linha
            coluna (int): Coordenada da coluna
        """
        self.__linha = linha
        self.__coluna = coluna
        self.__atingida = False
    
    @property
    def linha(self):
        """Retorna a linha da posicao."""
        return self.__linha
    
    @property
    def coluna(self):
        """Retorna a coluna da posicao."""
        return self.__coluna
    
    @property
    def atingida(self):
        """Retorna se a posicao foi atingida."""
        return self.__atingida
    
    @atingida.setter
    def atingida(self, valor):
        """Define se a posicao foi atingida."""
        self.__atingida = valor
    
    def __eq__(self, other):
        """
        Sobrecarga do operador de igualdade.
        """
        if isinstance(other, Posicao):
            return self.linha == other.linha and self.coluna == other.coluna
        return False
    
    def __str__(self):
        """
        Sobrecarga do operador de string.
        """
        return f"({self.linha}, {self.coluna})"

class Navio(ABC):
    """Classe abstrata base para todos os tipos de navios."""
    
    def __init__(self, tamanho, nome):
        """
        Inicializa um navio com tamanho e nome.
        
        Args:
            tamanho (int): Tamanho do navio
            nome (str): Nome do navio
        """
        self.__tamanho = tamanho
        self.__nome = nome
        self.__posicoes = []
        self.__orientacao = None  # 'horizontal' ou 'vertical'
    
    @property
    def tamanho(self):
        """Retorna o tamanho do navio."""
        return self.__tamanho
    
    @property
    def nome(self):
        """Retorna o nome do navio."""
        return self.__nome
    
    @property
    def posicoes(self):
        """Retorna as posicoes ocupadas pelo navio."""
        return self.__posicoes
    
    @property
    def orientacao(self):
        """Retorna a orientação do navio."""
        return self.__orientacao
    
    @orientacao.setter
    def orientacao(self, valor):
        """Define a orientação do navio."""
        self.__orientacao = valor
    
    def adicionar_posicao(self, posicao):
        """
        Adiciona uma posicao ao navio.
        
        Args:
            posicao (Posicao): posicao a ser adicionada
        """
        self.__posicoes.append(posicao)
    
    def esta_afundado(self):
        """
        Verifica se o navio está afundado.
        
        Returns:
            bool: True se todas as posicoes foram atingidas, False caso contrário
        """
        return all(posicao.atingida for posicao in self.__posicoes)
    
    def receber_tiro(self, posicao):
        """
        Recebe um tiro em uma posicao.
        
        Args:
            posicao (Posicao): posicao do tiro
        
        Returns:
            bool: True se o tiro acertou o navio, False caso contrário
        """
        for pos in self.__posicoes:
            if pos == posicao:
                pos.atingida = True
                return True
        return False
    
    def __str__(self):
        """
        Sobrecarga do operador de string.
        
        Returns:
            str: Representação string do navio
        """
        status = "afundado" if self.esta_afundado() else "ativo"
        return f"{self.nome} ({self.tamanho} posicoes) - {status}"

class PortaAvioes(Navio):
    """Representa um porta-avioes com 5 posicoes."""
    
    def __init__(self):
        """Inicializa um porta-avioes."""
        super().__init__(5, "Porta-Avioes")

class Encouracado(Navio):
    """Representa um encouraçado com 4 posicoes."""
    
    def __init__(self):
        """Inicializa um encouraçado."""
        super().__init__(4, "Encouraçado")

class Cruzador(Navio):
    """Representa um cruzador com 3 posicoes."""
    
    def __init__(self):
        """Inicializa um cruzador."""
        super().__init__(3, "Cruzador")

class Submarino(Navio):
    """Representa um submarino com 2 posicoes."""
    
    def __init__(self):
        """Inicializa um submarino."""
        super().__init__(2, "Submarino")

class Destroyer(Navio):
    """Representa um destroyer com 1 posicao."""
    
    def __init__(self):
        """Inicializa um destroyer."""
        super().__init__(1, "Destroyer")

class Tabuleiro:
    """Representa o tabuleiro do jogo."""
    
    def __init__(self, tamanho=10):
        """
        Inicializa um tabuleiro com tamanho específico.
        
        Args:
            tamanho (int, optional): Tamanho do tabuleiro. Padrão é 10.
        """
        self.__tamanho = tamanho
        self.__navios = []
        self.__tiros = []
    
    @property
    def tamanho(self):
        """Retorna o tamanho do tabuleiro."""
        return self.__tamanho
    
    @property
    def navios(self):
        """Retorna os navios no tabuleiro."""
        return self.__navios
    
    @property
    def tiros(self):
        """Retorna os tiros no tabuleiro."""
        return self.__tiros
    
    def adicionar_navio(self, navio, linha, coluna, orientacao):
        """
        Adiciona um navio ao tabuleiro.
        
        Args:
            navio (Navio): Navio a ser adicionado
            linha (int): Linha inicial do navio
            coluna (int): Coluna inicial do navio
            orientacao (str): Orientação do navio ('horizontal' ou 'vertical')
        
        Returns:
            bool: True se o navio foi adicionado com sucesso, False caso contrário
        """
        if not self.__posicao_valida(linha, coluna):
            return False
        
        # Verifica se o navio cabe no tabuleiro
        if orientacao == 'horizontal' and coluna + navio.tamanho > self.__tamanho:
            return False
        elif orientacao == 'vertical' and linha + navio.tamanho > self.__tamanho:
            return False
        
        # Verifica se há sobreposicao com outros navios
        posicoes = []
        if orientacao == 'horizontal':
            for i in range(navio.tamanho):
                pos = Posicao(linha, coluna + i)
                if self.__posicao_ocupada(pos):
                    return False
                posicoes.append(pos)
        else:  # vertical
            for i in range(navio.tamanho):
                pos = Posicao(linha + i, coluna)
                if self.__posicao_ocupada(pos):
                    return False
                posicoes.append(pos)
        
        # Adiciona o navio ao tabuleiro
        navio.orientacao = orientacao
        for pos in posicoes:
            navio.adicionar_posicao(pos)
        
        self.__navios.append(navio)
        return True
    
    def receber_tiro(self, linha, coluna):
        """
        Recebe um tiro no tabuleiro.
        
        Args:
            linha (int): Linha do tiro
            coluna (int): Coluna do tiro
        
        Returns:
            tuple: (bool, Navio) - True se acertou um navio, False caso contrário.
                   O navio atingido se houver, None caso contrário.
        """
        if not self.__posicao_valida(linha, coluna):
            return (False, None)
        
        posicao = Posicao(linha, coluna)
        
        # Verifica se já atirou nessa posicao
        for tiro in self.__tiros:
            if tiro == posicao:
                return (False, None)
        
        # Adiciona o tiro à lista de tiros
        self.__tiros.append(posicao)
        
        # Verifica se acertou algum navio
        for navio in self.__navios:
            if navio.receber_tiro(posicao):
                return (True, navio)
        
        return (False, None)
    
    def todos_navios_afundados(self):
        """
        Verifica se todos os navios estão afundados.
        
        Returns:
            bool: True se todos os navios estão afundados, False caso contrário
        """
        return all(navio.esta_afundado() for navio in self.__navios)
    
    def __posicao_valida(self, linha, coluna):
        """
        Verifica se uma posicao é válida no tabuleiro.
        
        Args:
            linha (int): Linha a ser verificada
            coluna (int): Coluna a ser verificada
        
        Returns:
            bool: True se a posicao é válida, False caso contrário
        """
        return 0 <= linha < self.__tamanho and 0 <= coluna < self.__tamanho
    
    def __posicao_ocupada(self, posicao):
        """
        Verifica se uma posicao está ocupada por um navio.
        
        Args:
            posicao (Posicao): posicao a ser verificada
        
        Returns:
            bool: True se a posicao está ocupada, False caso contrário
        """
        for navio in self.__navios:
            for pos in navio.posicoes:
                if pos == posicao:
                    return True
        return False
    
    def posicao_tem_tiro(self, linha, coluna):
        """
        Verifica se uma posicao já recebeu um tiro.
        
        Args:
            linha (int): Linha a ser verificada
            coluna (int): Coluna a ser verificada
        
        Returns:
            bool: True se a posicao já recebeu um tiro, False caso contrário
        """
        posicao = Posicao(linha, coluna)
        for tiro in self.__tiros:
            if tiro == posicao:
                return True
        return False
    
    def posicao_tem_navio_atingido(self, linha, coluna):
        """
        Verifica se uma posicao tem um navio atingido.
        
        Args:
            linha (int): Linha a ser verificada
            coluna (int): Coluna a ser verificada
        
        Returns:
            bool: True se a posicao tem um navio atingido, False caso contrário
        """
        posicao = Posicao(linha, coluna)
        for navio in self.__navios:
            for pos in navio.posicoes:
                if pos == posicao and pos.atingida:
                    return True
        return False
    
    def posicao_tem_navio(self, linha, coluna):
        """
        Verifica se uma posicao tem um navio.
        
        Args:
            linha (int): Linha a ser verificada
            coluna (int): Coluna a ser verificada
        
        Returns:
            bool: True se a posicao tem um navio, False caso contrário
        """
        posicao = Posicao(linha, coluna)
        for navio in self.__navios:
            for pos in navio.posicoes:
                if pos == posicao:
                    return True
        return False