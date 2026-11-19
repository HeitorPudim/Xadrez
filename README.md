# ♟️ Xadrez

Um programa de xadrez com interface gráfica, integração com o motor Stockfish e recursos de análise de partidas e posições.

## 📋 Sobre o Projeto

O **Xadrez** é um projeto pessoal de xadrez desenvolvido em Python que combina:

- **Interface gráfica** completa com Tkinter
- **Motor de xadrez Stockfish** para análise de posições
- **Análise de melhores jogadas** com as 3 opções principais
- **Visualização de variações** com setas coloridas no tabuleiro
- **Suporte a todas as regras oficiais** de xadrez (incluindo roque, promoção, etc.)

## ✨ Funcionalidades

### Interface Gráfica
- Tabuleiro visual com peças Unicode
- Escolha de cor: joga de brancas ou pretas
- Inversão automática do tabuleiro para o lado das pretas
- Coordenadas visuais (letras a-h, números 1-8)
- Destaque de movimentos válidos ao selecionar uma peça

### Análise com IA
- Integração com o motor Stockfish (um dos mais fortes do mundo)
- Mostra as 3 melhores jogadas com suas avaliações
- Setas coloridas no tabuleiro:
  - 🔴 Vermelho: 1ª melhor jogada
  - 🔵 Azul: 2ª melhor jogada
  - 🟢 Verde: 3ª melhor jogada
- Exibição de linhas de variação (5 jogadas de cada opção)

### Modo de Jogo
- Jogue contra o adversário (modo humano)
- Digite as jogadas do adversário manualmente
- Use o botão "Fazer melhor jogada" para que o programa jogue por você
- Modo de linha de comando (`main.py`) para uso em terminal

## 🛠️ Tecnologias

| Tecnologia | Versão | Descrição |
|---|---|---|
| Python | 3.14+ | Linguagem de programação principal |
| python-chess | 1.999 | Biblioteca para trabalhar com posições e movimentos |
| Tkinter | (padrão) | Interface gráfica |
| Stockfish | (incluído) | Motor de xadrez de alta performance |

## 📦 Instalação

### Pré-requisitos

1. **Python 3.14+** instalado
2. **Stockfish** baixado (veja abaixo)

### Passo a passo

```bash
# 1. Clone ou baixe o repositório
git clone https://github.com/seu-usuario/Xadrez.git
cd xadrez

# 2. Instale as dependências Python
python -m pip install -r requirements.txt

# 3. Baixe o Stockfish
# Visite: https://github.com/official-stockfish/Stockfish/releases
# E baixe a versão para o seu sistema operacional
# Coloque o executável na pasta stockfish/
```

### Estrutura do Stockfish

O Stockfish é distribuído separadamente. Baixe a versão apropriada para seu sistema e coloque na pasta `stockfish/`:

| Sistema | Arquivo Esperado |
|---|---|
| Windows | `stockfish-windows-x86-64-avx2.exe` |
| Linux | `stockfish-linux-x86-64-avx2` |
| macOS | `stockfish-mac-x86-64-avx2` |

## 🚀 Execução

### Interface Gráfica

```bash
python tabuleiro.py
```

### Modo Linha de Comando

```bash
python main.py
```

## 📄 Licenças

### Projeto Xadrez
Este projeto é de autoria pessoal e está sob licença [MIT](LICENSE) (a ser definida).

### Stockfish
O motor Stockfish é distribuído sob **GNU General Public License v3 (GPLv3)**. Veja o arquivo `stockfish/COPYing.txt` para detalhes completos.

### python-chess
A biblioteca python-chess é distribuído sob licença BSD de 2 clause. Veja https://github.com/niklasf/python-chess para mais informações.

## 🤝 Contribuições

Este é um projeto pessoal. Se você deseja contribuir, sinta-se livre para fazer pull requests.

## 📝 Agradecimentos

- [Stockfish](https://stockfishchess.org/) — pelo excelente motor de xadrez
- [python-chess](https://python-chess.readthedocs.io/) — pela fantastic biblioteca
- [Tkinter](https://docs.python.org/3/library/tkinter.html) — pela interface gráfica

---

**Estudante de Ciência da Computação** 🎓
