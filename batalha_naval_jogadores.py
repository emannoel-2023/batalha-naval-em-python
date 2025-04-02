from abc import ABC, abstractmethod
import random
from batalha_naval_classes import Posicao, Tabuleiro, PortaAvioes, Encouracado, Cruzador, Submarino, Destroyer

class Jogador(ABC):
    """Classe abstrata base para todos os jogadores."""
    
    def __init__(self, nome):
        """
        Inicializa um jogador com nome e tabuleiro.
        
        Args:
            nome (str): Nome do jogador
        """
        self.__nome = nome
        self.__tabuleiro = Tabuleiro()
        self.__tabuleiro_oponente = Tabuleiro()  # Tabuleiro para rastrear os tiros contra o oponente
    
    @property
    def nome(self):
        """Retorna o nome do jogador."""
        return self.__nome
    
    @property
    def tabuleiro(self):
        """Retorna o tabuleiro do jogador."""
        return self.__tabuleiro
    
    @property
    def tabuleiro_oponente(self):
        """Retorna o tabuleiro do oponente do jogador."""
        return self.__tabuleiro_oponente
    
    def inicializar_frota(self):
        """Inicializa a frota do jogador."""
        self._adicionar_navios()
    
    @abstractmethod
    def _adicionar_navios(self):
        """Metodo abstrato para adicionar navios ao tabuleiro."""
        pass
    
    @abstractmethod
    def fazer_jogada(self):
        """
        Metodo abstrato para fazer uma jogada.
        
        Returns:
            tuple: (int, int) - Coordenadas da jogada (linha, coluna)
        """
        pass
    
    def registrar_resultado_tiro(self, linha, coluna, acertou, navio_afundado=None):
        """
        Registra o resultado de um tiro no tabuleiro do oponente.
        
        Args:
            linha (int): Linha do tiro
            coluna (int): Coluna do tiro
            acertou (bool): True se acertou um navio, False caso contrario
            navio_afundado (Navio, optional): Navio afundado se houver. Padrao eh None.
        """
        self.__tabuleiro_oponente.receber_tiro(linha, coluna)
    
    def perdeu(self):
        """
        Verifica se o jogador perdeu.
        
        Returns:
            bool: True se todos os navios do jogador estao afundados, False caso contrário
        """
        return self.__tabuleiro.todos_navios_afundados()

class JogadorHumano(Jogador):
    """Representa um jogador humano."""
    
    def __init__(self, nome="Jogador"):
        """
        Inicializa um jogador humano.
        
        Args:
            nome (str, optional): Nome do jogador. Padrao eh "Jogador".
        """
        super().__init__(nome)
    
    def _adicionar_navios(self):
        """Adiciona os navios ao tabuleiro do jogador humano."""
        # Será implementado na interface do jogo
        pass
    
    def fazer_jogada(self):
        """
        Implementacao do metodo abstrato fazer_jogada.
        Sera chamado pela interface do jogo.
        
        Returns:
            tuple: (int, int) - Coordenadas da jogada (linha, coluna)
        """
        # Será implementado na interface do jogo
        pass

class JogadorIA(Jogador):
    """Representa um jogador controlado por IA."""
    
    def __init__(self, nome="Computador"):
        """
        Inicializa um jogador IA.
        
        Args:
            nome (str, optional): Nome do jogador. Padrao eh "Computador".
        """
        super().__init__(nome)
        self.__tiros_acertados = []
        self.__tiros_pendentes = []
    
    def _adicionar_navios(self):
        """Adiciona os navios ao tabuleiro do jogador IA de forma aleatoria."""
        navios = [
            PortaAvioes(),
            Encouracado(),
            Cruzador(),
            Submarino(),
            Destroyer()
        ]
        
        for navio in navios:
            while True:
                linha = random.randint(0, self.tabuleiro.tamanho - 1)
                coluna = random.randint(0, self.tabuleiro.tamanho - 1)
                orientacao = random.choice(['horizontal', 'vertical'])
                
                if self.tabuleiro.adicionar_navio(navio, linha, coluna, orientacao):
                    break
    
    def fazer_jogada(self):
        """
        Implementa a lógica de jogada da IA.
        
        Returns:
            tuple: (int, int) - Coordenadas da jogada (linha, coluna)
        """
        # Se há tiros pendentes (áreas ao redor de acertos anteriores), tenta-os primeiro
        if self.__tiros_pendentes:
            linha, coluna = self.__tiros_pendentes.pop(0)
            return linha, coluna
        
        # Se há tiros acertados, tenta atirar ao redor deles
        if self.__tiros_acertados:
            ultima_linha, ultima_coluna = self.__tiros_acertados[-1]
            possiveis_tiros = []
            
            # Tenta atirar nas quatro direcoes adjacentes
            direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # cima, baixo, esquerda, direita
            
            for dl, dc in direcoes:
                nova_linha, nova_coluna = ultima_linha + dl, ultima_coluna + dc
                
                # Verifica se a posição é válida e não foi atingida antes
                if (0 <= nova_linha < self.tabuleiro_oponente.tamanho and 
                    0 <= nova_coluna < self.tabuleiro_oponente.tamanho and 
                    not self.tabuleiro_oponente.posicao_tem_tiro(nova_linha, nova_coluna)):
                    possiveis_tiros.append((nova_linha, nova_coluna))
            
            # Se há tiros possíveis, adiciona à lista de pendentes e usa o primeiro
            if possiveis_tiros:
                self.__tiros_pendentes.extend(possiveis_tiros)
                linha, coluna = self.__tiros_pendentes.pop(0)
                return linha, coluna
        
        # Caso contrário, faz um tiro aleatório
        while True:
            linha = random.randint(0, self.tabuleiro_oponente.tamanho - 1)
            coluna = random.randint(0, self.tabuleiro_oponente.tamanho - 1)
            
            if not self.tabuleiro_oponente.posicao_tem_tiro(linha, coluna):
                return linha, coluna
    
    def registrar_resultado_tiro(self, linha, coluna, acertou, navio_afundado=None):
        """
        Registra o resultado de um tiro no tabuleiro do oponente.
        
        Args:
            linha (int): Linha do tiro
            coluna (int): Coluna do tiro
            acertou (bool): True se acertou um navio, False caso contrario
            navio_afundado (Navio, optional): Navio afundado se houver. Padrao eh None.
        """
        super().registrar_resultado_tiro(linha, coluna, acertou, navio_afundado)
        
        if acertou:
            self.__tiros_acertados.append((linha, coluna))
        elif navio_afundado:
            # Se afundou um navio, limpa os tiros acertados e pendentes
            # para começar a procurar um novo navio
            self.__tiros_acertados.clear()
            self.__tiros_pendentes.clear()