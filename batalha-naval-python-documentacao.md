# Documentação do Jogo Batalha Naval em Python

## Visão Geral

Este projeto implementa o clássico jogo de tabuleiro Batalha Naval em Python, com uma interface de linha de comando. O jogador pode posicionar seus navios no tabuleiro e competir contra uma IA simples, seguindo as regras tradicionais do jogo.

## Estrutura do Projeto

O código está organizado em três arquivos principais:

1. **batalha_naval_classes.py** - Define as classes fundamentais do jogo
2. **batalha_naval_jogadores.py** - Implementa os tipos de jogadores
3. **batalha_naval_jogo.py** - Contém a lógica de jogo e interface com o usuário

## Descrição dos Componentes

### batalha_naval_classes.py

Este arquivo define as estruturas básicas do jogo:

#### Classe `Posicao`
Representa uma coordenada no tabuleiro:
- `linha` e `coluna` - coordenadas no tabuleiro
- `atingida` - status que indica se a posição já foi atingida por um tiro

#### Classe `Navio` (Abstrata)
Classe base para todos os tipos de navios:
- `tamanho` - quantidade de posições que o navio ocupa
- `nome` - identificação do navio
- `posicoes` - lista de objetos Posicao ocupados pelo navio
- `orientacao` - "horizontal" ou "vertical"

Principais métodos:
- `adicionar_posicao()` - adiciona uma posição ao navio
- `esta_afundado()` - verifica se todas as posições foram atingidas
- `receber_tiro()` - processa um tiro recebido

#### Tipos de Navios
Implementados como subclasses de `Navio`:
- `PortaAvioes` - ocupa 5 posições
- `Encouracado` - ocupa 4 posições
- `Cruzador` - ocupa 3 posições
- `Submarino` - ocupa 2 posições
- `Destroyer` - ocupa 1 posição

#### Classe `Tabuleiro`
Gerencia o tabuleiro do jogo:
- `tamanho` - dimensão do tabuleiro (padrão: 10x10)
- `navios` - lista de navios no tabuleiro
- `tiros` - registro de tiros realizados

Principais métodos:
- `adicionar_navio()` - posiciona um navio no tabuleiro
- `receber_tiro()` - processa um tiro nas coordenadas especificadas
- `todos_navios_afundados()` - verifica se todos os navios foram destruídos

### batalha_naval_jogadores.py

Define os tipos de jogadores:

#### Classe `Jogador` (Abstrata)
Base para implementações específicas de jogadores:
- `tabuleiro` - tabuleiro com os navios do jogador
- `tabuleiro_oponente` - tabuleiro para rastrear tiros contra o oponente

Métodos principais:
- `inicializar_frota()` - adiciona navios ao tabuleiro
- `fazer_jogada()` - método abstrato para realizar uma jogada
- `perdeu()` - verifica se todos os navios foram afundados

#### Classe `JogadorHumano`
Implementação para jogador controlado por humano:
- Métodos para adicionar navios e realizar jogadas são implementados na interface do jogo

#### Classe `JogadorIA`
Implementação para jogador controlado por computador:
- Posiciona navios aleatoriamente
- Implementa uma estratégia simples de ataque:
  - Inicia com tiros aleatórios
  - Quando acerta um navio, tenta atirar nas posições adjacentes
  - Mantém uma lista de tiros pendentes ao redor de acertos anteriores

### batalha_naval_jogo.py

Implementa a lógica do jogo e interface com usuário:

#### Classe `Jogo`
Controla o fluxo do jogo:
- Inicialização e configuração
- Gerenciamento de turnos
- Exibição do estado do jogo
- Processamento do fim de jogo

Métodos principais:
- `iniciar()` - inicia o jogo
- `__configurar_jogo()` - configura os jogadores e navios
- `__jogar()` - implementa o loop principal do jogo
- `__turno_jogador_humano()` e `__turno_jogador_ia()` - processam os turnos
- `__mostrar_tabuleiro()` - exibe representação visual do tabuleiro

#### Classe `InterfaceJogo`
Gerencia a experiência do usuário:
- Exibe menu principal
- Mostra instruções e regras
- Inicia novos jogos

## Como Executar o Jogo

1. Certifique-se de que os três arquivos estejam no mesmo diretório:
   - `batalha_naval_classes.py`
   - `batalha_naval_jogadores.py`
   - `batalha_naval_jogo.py`

2. Execute o arquivo principal com Python:
   ```
   python batalha_naval_jogo.py
   ```

3. Siga as instruções na tela para jogar.

## Fluxo do Jogo

1. **Tela inicial**: Apresenta as regras e instruções
2. **Posicionamento dos navios**: O jogador posiciona seus navios no tabuleiro
   - Para cada navio, escolha:
     - Orientação (h - horizontal, v - vertical)
     - Coordenadas iniciais (linha,coluna)
3. **Fase de jogo**: Os jogadores alternam turnos, escolhendo coordenadas para atacar
4. **Final de jogo**: O jogo termina quando todos os navios de um jogador são afundados

## Legenda do Tabuleiro

- `~` : Água (posição não atacada)
- `O` : Água (tiro na água)
- `N` : Navio (apenas visível no seu tabuleiro)
- `X` : Navio atingido

## Requisitos do Sistema

- Python 3.x
- Compatível com Windows, macOS e Linux

## Conclusão

Este projeto demonstra uma implementação completa do jogo Batalha Naval usando princípios de programação orientada a objetos. A estrutura modular facilita a manutenção e possíveis extensões do código, como a adição de novos tipos de jogadores ou interfaces gráficas.
