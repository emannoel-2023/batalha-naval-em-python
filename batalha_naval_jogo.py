import os
import time
from batalha_naval_classes import Tabuleiro, PortaAvioes, Encouracado, Cruzador, Submarino, Destroyer
from batalha_naval_jogadores import JogadorHumano, JogadorIA

class Jogo:
    """Classe principal que controla o fluxo do jogo."""
    
    def __init__(self):
        """Inicializa o jogo."""
        self.__jogador_humano = JogadorHumano("Jogador")
        self.__jogador_ia = JogadorIA("Computador")
        self.__jogador_atual = self.__jogador_humano
        self.__em_execucao = False
    
    def iniciar(self):
        """Inicia o jogo."""
        self.__em_execucao = True
        self.__mostrar_titulo()
        self.__configurar_jogo()
        self.__jogar()
    
    def __mostrar_titulo(self):
        """Exibe o titulo do jogo."""
        self.__limpar_tela()
        print("=" * 50)
        print("             BATALHA NAVAL")
        print("=" * 50)
        print()
        input("Pressione ENTER para continuar...")
    
    def __configurar_jogo(self):
        """Configura o jogo, posicionando os navios."""
        self.__limpar_tela()
        print("Configuracao do Jogo")
        print("===================")
        print()
        
        # Posiciona os navios da IA
        self.__jogador_ia.inicializar_frota()
        
        # Posiciona os navios do jogador humano
        self.__posicionar_navios_jogador()
    
    def __posicionar_navios_jogador(self):
        """Permite ao jogador posicionar seus navios."""
        navios = [
            PortaAvioes(),
            Encouracado(),
            Cruzador(),
            Submarino(),
            Destroyer()
        ]
        
        for navio in navios:
            while True:
                self.__limpar_tela()
                print(f"Posicionando {navio.nome} ({navio.tamanho} posicoes)")
                print()
                self.__mostrar_tabuleiro_jogador()
                print()
                
                try:
                    orientacao = self.__obter_orientacao()
                    linha, coluna = self.__obter_coordenadas()
                    
                    if self.__jogador_humano.tabuleiro.adicionar_navio(navio, linha, coluna, orientacao):
                        break
                    else:
                        print("Nao eh possivel posicionar o navio nessa posicao.")
                        print("Verifique se nao tem sobreposicao com outros navios ou se o navio nao ultrapassa o tabuleiro.")
                        input("Pressione ENTER para tentar novamente...")
                except ValueError as e:
                    print(f"Erro: {e}")
                    input("Pressione ENTER para tentar novamente...")
    
    def __obter_orientacao(self):
        """
        Obtem a orientacão do navio do jogador.
        
        Returns:
            str: 'horizontal' ou 'vertical'
        """
        while True:
            orientacao = input("Orientacao (h - horizontal, v - vertical): ").strip().lower()
            if orientacao == 'h':
                return 'horizontal'
            elif orientacao == 'v':
                return 'vertical'
            else:
                print("Orientacao invalida. Use 'h' para horizontal ou 'v' para vertical.")
    
    def __obter_coordenadas(self):
        """
        Obtem as coordenadas do jogador.
        
        Returns:
            tuple: (int, int) - Coordenadas (linha, coluna)
        """
        while True:
            try:
                coords = input("Coordenadas (linha,coluna): ").strip().split(',')
                if len(coords) != 2:
                    raise ValueError("Formato invalido. Use 'linha,coluna'.")
                
                linha = int(coords[0])
                coluna = int(coords[1])
                
                if not (0 <= linha < self.__jogador_humano.tabuleiro.tamanho and 
                        0 <= coluna < self.__jogador_humano.tabuleiro.tamanho):
                    raise ValueError(f"Coordenadas fora do tabuleiro. Use valores entre 0 e {self.__jogador_humano.tabuleiro.tamanho - 1}.")
                
                return linha, coluna
            except ValueError as e:
                print(f"Erro: {e}")
    
    def __jogar(self):
        """Implementa o loop principal do jogo."""
        while self.__em_execucao:
            self.__limpar_tela()
            self.__mostrar_status_jogo()
            
            # Verifica se o jogador quer sair
            if self.__jogador_atual == self.__jogador_humano:
                print("Opcoes: ")
                print("1. Fazer um tiro")
                print("2. Sair do jogo")
                
                opcao = input("Escolha uma opcao (1-2): ").strip()
                
                if opcao == "2":
                    print("Saindo do jogo...")
                    self.__em_execucao = False
                    break
                elif opcao != "1":
                    print("Opcao invalida. Tente novamente.")
                    input("Pressione ENTER para continuar...")
                    continue
                
                self.__turno_jogador_humano()
                if self.__jogador_ia.perdeu():
                    self.__fim_de_jogo(True)
                    break
                self.__jogador_atual = self.__jogador_ia
            else:
                self.__turno_jogador_ia()
                if self.__jogador_humano.perdeu():
                    self.__fim_de_jogo(False)
                    break
                self.__jogador_atual = self.__jogador_humano
    
    def __turno_jogador_humano(self):
        """Processa o turno do jogador humano."""
        print("Seu turno!")
        print("Selecione uma posicao para atacar:")
        
        while True:
            try:
                linha, coluna = self.__obter_coordenadas()
                
                if self.__jogador_humano.tabuleiro_oponente.posicao_tem_tiro(linha, coluna):
                    print("Você ja atirou nessa posicão. Escolha outra.")
                    continue
                
                break
            except ValueError as e:
                print(f"Erro: {e}")
        
        acertou, navio = self.__jogador_ia.tabuleiro.receber_tiro(linha, coluna)
        self.__jogador_humano.registrar_resultado_tiro(linha, coluna, acertou, navio if acertou else None)
        
        self.__limpar_tela()
        self.__mostrar_status_jogo()
        
        if acertou:
            print("Voce ACERTOU um navio!")
            if navio.esta_afundado():
                print(f"Voce afundou o {navio.nome} do oponente!")
        else:
            print("Voce errou.")
        
        input("Pressione ENTER para continuar...")
    
    def __turno_jogador_ia(self):
        """Processa o turno do jogador IA."""
        print("Turno do computador...")
        time.sleep(1)
        
        linha, coluna = self.__jogador_ia.fazer_jogada()
        acertou, navio = self.__jogador_humano.tabuleiro.receber_tiro(linha, coluna)
        self.__jogador_ia.registrar_resultado_tiro(linha, coluna, acertou, navio if acertou else None)
        
        self.__limpar_tela()
        self.__mostrar_status_jogo()
        
        print(f"O computador atirou em ({linha}, {coluna}).")
        
        if acertou:
            print("O computador ACERTOU um dos seus navios!")
            if navio.esta_afundado():
                print(f"O computador afundou o seu {navio.nome}!")
        else:
            print("O computador errou.")
        
        input("Pressione ENTER para continuar...")
    
    def __fim_de_jogo(self, vitoria):
        """
        Processa o fim do jogo.
        
        Args:
            vitoria (bool): True se o jogador humano venceu, False caso contrário
        """
        self.__limpar_tela()
        print("=" * 50)
        if vitoria:
            print("              VOCE VENCEU!")
        else:
            print("              VOCE PERDEU!")
        print("=" * 50)
        print()
        print("Situacao final dos tabuleiros:")
        print()
        
        print("Seu tabuleiro:")
        self.__mostrar_tabuleiro_jogador(mostrar_navios=True)
        print()
        
        print("Tabuleiro do computador:")
        self.__mostrar_tabuleiro_oponente(mostrar_navios=True)
        print()
        
        self.__em_execucao = False
        input("Pressione ENTER para encerrar o jogo...")
    
    def __mostrar_status_jogo(self):
        """Exibe o status atual do jogo."""
        print("BATALHA NAVAL")
        print("=============")
        print()
        
        print("Seu tabuleiro:")
        self.__mostrar_tabuleiro_jogador()
        print()
        
        print("Tabuleiro do oponente:")
        self.__mostrar_tabuleiro_oponente()
        print()
    
    def __mostrar_tabuleiro_jogador(self, mostrar_navios=True):
        """
        Exibe o tabuleiro do jogador.
        
        Args:
            mostrar_navios (bool, optional): Se True, mostra os navios. Padrão é True.
        """
        tabuleiro = self.__jogador_humano.tabuleiro
        self.__mostrar_tabuleiro(tabuleiro, mostrar_navios)
    
    def __mostrar_tabuleiro_oponente(self, mostrar_navios=False):
        """
        Exibe o tabuleiro do oponente.
        
        Args:
            mostrar_navios (bool, optional): Se True, mostra os navios. Padrão é False.
        """
        tabuleiro = self.__jogador_ia.tabuleiro
        tabuleiro_visivel = self.__jogador_humano.tabuleiro_oponente
        self.__mostrar_tabuleiro(tabuleiro, mostrar_navios, tabuleiro_visivel)
    
    def __mostrar_tabuleiro(self, tabuleiro, mostrar_navios=False, tabuleiro_visivel=None):
        """
        Exibe um tabuleiro.
        
        Args:
            tabuleiro (Tabuleiro): Tabuleiro a ser exibido
            mostrar_navios (bool, optional): Se True, mostra os navios. Padrão é False.
            tabuleiro_visivel (Tabuleiro, optional): Tabuleiro com informac0es visíveis. Padrão é None.
        """
        # Exibe as coordenadas das colunas
        print("  ", end="")
        for j in range(tabuleiro.tamanho):
            print(f" {j} ", end="")
        print()
        
        # Exibe as linhas do tabuleiro
        for i in range(tabuleiro.tamanho):
            print(f"{i} ", end="")
            
            for j in range(tabuleiro.tamanho):
                # Verifica se a posicão foi atingida e tem um navio
                if tabuleiro.posicao_tem_tiro(i, j) and tabuleiro.posicao_tem_navio(i, j):
                    print(" X ", end="")
                # Verifica se a posicão foi atingida mas não tem navio
                elif tabuleiro.posicao_tem_tiro(i, j):
                    print(" O ", end="")
                # Verifica se a posicão tem um navio e deve ser mostrada
                elif mostrar_navios and tabuleiro.posicao_tem_navio(i, j):
                    print(" N ", end="")
                # Verifica se estamos usando um tabuleiro visível (para o oponente)
                elif tabuleiro_visivel and tabuleiro_visivel.posicao_tem_tiro(i, j):
                    if tabuleiro.posicao_tem_navio(i, j):
                        print(" X ", end="")
                    else:
                        print(" O ", end="")
                # Caso contrário, mostra uma posicão vazia
                else:
                    print(" ~ ", end="")
            
            print()
    
    def __limpar_tela(self):
        """Limpa a tela do console."""
        # Para Windows
        if os.name == 'nt':
            os.system('cls')
        # Para Mac e Linux
        else:
            os.system('clear')

class InterfaceJogo:
    """Classe responsavel pela interface do jogo com o usuario."""
    
    def __init__(self):
        """Inicializa a interface do jogo."""
        pass
    
    def iniciar(self):
        """Inicia a interface do jogo."""
        self.__mostrar_boas_vindas()
        self.__menu_principal()
        self.__mostrar_despedida()
    
    def __menu_principal(self):
        """Exibe o menu principal do jogo."""
        while True:
            self.__limpar_tela()
            print("MENU PRINCIPAL")
            print("=============")
            print()
            print("1. Iniciar novo jogo")
            print("2. Sair")
            print()
            opcao = input("Escolha uma opcao (1-2): ").strip()
            
            if opcao == "1":
                jogo = Jogo()
                jogo.iniciar()
            elif opcao == "2":
                return
            else:
                print("Opcao invalida. Tente novamente.")
                input("Pressione ENTER para continuar...")
    
    def __mostrar_boas_vindas(self):
        """Exibe a mensagem de boas-vindas."""
        self.__limpar_tela()
        print("""
    ____        __        ____             _   __                  __
   / __ )____ _/ /_____ _/ / /_  ____ _   / | / /___ __   ______ _/ /
  / __  / __ `/ __/ __ `/ / __ \/ __ `/  /  |/ / __ `/ | / / __ `/ / 
 / /_/ / /_/ / /_/ /_/ / / / / / /_/ /  / /|  / /_/ /| |/ / /_/ / /  
/_____/\__,_/\__/\__,_/_/_/ /_/\__,_/  /_/ |_/\__,_/ |___/\__,_/_/   
        """)
        print("=" * 50)
        print()
        print("Bem-vindo ao jogo de Batalha Naval!")
        print("Regras do jogo:")
        print("1. Voce e o computador possuem navios posicionados em um tabuleiro 10x10.")
        print("2. Voces alternam turnos, tentando acertar os navios adversarios.")
        print("3. O primeiro a afundar todos os navios adversarios vence.")
        print()
        print("Tipos de navios:")
        print("- Porta-Avioes: 5 posicoes")
        print("- Encouracado: 4 posicoes")
        print("- Cruzador: 3 posicoes")
        print("- Submarino: 2 posicoes")
        print("- Destroyer: 1 posicao")
        print()
        print("Legenda do tabuleiro:")
        print("~ : Agua (posicao nao atacada)")
        print("O : Agua (tiro na agua)")
        print("N : Navio (apenas visivel no seu tabuleiro)")
        print("X : Navio atingido")
        print()
        input("Pressione ENTER para continuar...")
    
    def __mostrar_despedida(self):
        """Exibe a mensagem de despedida."""
        self.__limpar_tela()
        print()
        print("Obrigado por jogar Batalha Naval!")
        print()
        input("Pressione ENTER para sair...")
    
    def __limpar_tela(self):
        """Limpa a tela do console."""
        # Para Windows
        if os.name == 'nt':
            os.system('cls')
        # Para Mac e Linux
        else:
            os.system('clear')

# Arquivo principal para executar o jogo
if __name__ == "__main__":
    interface = InterfaceJogo()
    interface.iniciar()