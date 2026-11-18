# python -m pip install python-chess
import tkinter as tk
import chess
import chess.engine


# Caminho do Stockfish
caminho_stockfish = r"C:\Users\heito\OneDrive\Documentos\xadrez_ia\stockfish\stockfish-windows-x86-64-universal"


# Cria a janela
janela = tk.Tk()

janela.title("Xadrez IA")
janela.geometry("700x880")


# Tamanho das casas
tamanho = 80

# Espaço para as letras e números
margem = 25


# Tamanho do tabuleiro visual
tamanho_tabuleiro = tamanho * 8


# Cria o tabuleiro visual
canvas = tk.Canvas(
    janela,
    width=tamanho_tabuleiro + margem,
    height=tamanho_tabuleiro + margem
)

canvas.pack()


# Cria o tabuleiro do python-chess
tabuleiro = chess.Board()


# Cor do jogador
minha_cor = chess.WHITE


# Guarda as melhores jogadas encontradas
melhor_jogada = None
segunda_jogada = None
terceira_jogada = None


# Guarda a peça selecionada
casa_selecionada = None


# Abre o Stockfish
engine = chess.engine.SimpleEngine.popen_uci(caminho_stockfish)

engine.configure({
    "Threads": 4,
    "Hash": 512
})


def escolher_cor(cor):

    global minha_cor
    global casa_selecionada
    global melhor_jogada
    global segunda_jogada
    global terceira_jogada

    minha_cor = cor

    # Cancela seleção e análise anterior
    casa_selecionada = None
    melhor_jogada = None
    segunda_jogada = None
    terceira_jogada = None

    if cor == chess.WHITE:
        texto_cor.config(text="Você joga de: Brancas")

    else:
        texto_cor.config(text="Você joga de: Pretas")

    desenhar_tabuleiro()

    atualizar_turno()


def atualizar_turno():

    if tabuleiro.turn == minha_cor:

        texto_turno.config(
            text="Sua vez"
        )

    else:

        texto_turno.config(
            text="Vez do adversário"
        )


def obter_casa_clicada(event):

    # Retira a margem das coordenadas
    x = event.x - margem
    y = event.y

    # Clique fora do tabuleiro
    if x < 0 or y < 0:
        return None

    if x >= tamanho_tabuleiro or y >= tamanho_tabuleiro:
        return None

    coluna = x // tamanho
    linha = y // tamanho

    # Quando joga de pretas, o tabuleiro visual está invertido
    if minha_cor == chess.WHITE:

        casa = chess.square(
            coluna,
            7 - linha
        )

    else:

        casa = chess.square(
            7 - coluna,
            linha
        )

    return casa


def obter_posicao_visual(casa):

    coluna = chess.square_file(casa)
    linha = chess.square_rank(casa)

    # Tabuleiro normal
    if minha_cor == chess.WHITE:

        coluna_visual = coluna
        linha_visual = 7 - linha

    # Tabuleiro invertido
    else:

        coluna_visual = 7 - coluna
        linha_visual = linha

    return coluna_visual, linha_visual


def clicar_tabuleiro(event):

    global casa_selecionada
    global melhor_jogada
    global segunda_jogada
    global terceira_jogada

    # Descobre qual casa foi clicada
    casa = obter_casa_clicada(event)

    # Clique fora do tabuleiro
    if casa is None:
        return

    # Primeiro clique: seleciona a peça
    if casa_selecionada is None:

        peca = tabuleiro.piece_at(casa)

        # Não existe peça nessa casa
        if peca is None:

            resultado.config(
                text="Clique em uma peça."
            )

            return

        # A peça precisa ser da cor que está jogando
        if peca.color != tabuleiro.turn:

            resultado.config(
                text="Essa peça não pode jogar agora."
            )

            return

        casa_selecionada = casa

        resultado.config(
            text="Agora clique na casa de destino."
        )

        desenhar_tabuleiro()

        destacar_casa(casa_selecionada)

        destacar_movimentos(casa_selecionada)

    # Segundo clique: tenta fazer o movimento
    else:

        movimento = chess.Move(
            casa_selecionada,
            casa
        )

        # Verifica promoção de peão
        peca = tabuleiro.piece_at(casa_selecionada)

        if peca is not None and peca.piece_type == chess.PAWN:

            linha_destino = chess.square_rank(casa)

            if linha_destino == 0 or linha_destino == 7:

                movimento = chess.Move(
                    casa_selecionada,
                    casa,
                    promotion=chess.QUEEN
                )

        # Verifica se o movimento é legal
        if movimento in tabuleiro.legal_moves:

            tabuleiro.push(movimento)

            casa_selecionada = None

            # Apaga as setas antigas
            melhor_jogada = None
            segunda_jogada = None
            terceira_jogada = None

            desenhar_tabuleiro()

            atualizar_turno()

            resultado.config(
                text="Jogada realizada!"
            )

        else:

            # Se clicou em outra peça da mesma cor,
            # troca a seleção para essa peça
            peca_nova = tabuleiro.piece_at(casa)

            if peca_nova is not None and peca_nova.color == tabuleiro.turn:

                casa_selecionada = casa

                desenhar_tabuleiro()

                destacar_casa(casa_selecionada)

                destacar_movimentos(casa_selecionada)

                resultado.config(
                    text="Peça selecionada."
                )

            else:

                resultado.config(
                    text="Movimento inválido."
                )

                casa_selecionada = None

                desenhar_tabuleiro()


def destacar_casa(casa):

    coluna, linha = obter_posicao_visual(casa)

    x1 = margem + coluna * tamanho
    y1 = linha * tamanho
    x2 = x1 + tamanho
    y2 = y1 + tamanho

    canvas.create_rectangle(
        x1,
        y1,
        x2,
        y2,
        outline="yellow",
        width=4
    )


def destacar_movimentos(casa):

    # Percorre todas as jogadas legais
    for movimento in tabuleiro.legal_moves:

        # Verifica se a jogada começa na peça selecionada
        if movimento.from_square == casa:

            destino = movimento.to_square

            coluna, linha = obter_posicao_visual(destino)

            x = margem + coluna * tamanho + tamanho / 2
            y = linha * tamanho + tamanho / 2

            # Verifica se existe uma peça no destino
            peca_destino = tabuleiro.piece_at(destino)

            if peca_destino is None:

                # Casa vazia
                canvas.create_oval(
                    x - 10,
                    y - 10,
                    x + 10,
                    y + 10,
                    fill="yellow",
                    outline=""
                )

            else:

                # Casa onde existe uma peça que pode ser capturada
                x1 = margem + coluna * tamanho + 5
                y1 = linha * tamanho + 5
                x2 = x1 + tamanho - 10
                y2 = y1 + tamanho - 10

                canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    outline="yellow",
                    width=4
                )


def desenhar_seta(jogada, cor, largura):

    # Se não existe jogada, não faz nada
    if jogada is None:
        return

    # Descobre a casa de origem
    origem = jogada.from_square

    # Descobre a casa de destino
    destino = jogada.to_square

    # Converte as casas para a posição visual
    coluna_origem, linha_origem = obter_posicao_visual(origem)
    coluna_destino, linha_destino = obter_posicao_visual(destino)

    # Centro da casa de origem
    x1 = margem + coluna_origem * tamanho + tamanho / 2
    y1 = linha_origem * tamanho + tamanho / 2

    # Centro da casa de destino
    x2 = margem + coluna_destino * tamanho + tamanho / 2
    y2 = linha_destino * tamanho + tamanho / 2

    # Desenha a seta
    canvas.create_line(
        x1,
        y1,
        x2,
        y2,
        fill=cor,
        width=largura,
        arrow=tk.LAST,
        arrowshape=(16, 20, 6)
    )


def desenhar_setas_melhores_jogadas():

    # 3ª melhor primeiro
    # Assim as setas mais importantes ficam por cima
    desenhar_seta(
        terceira_jogada,
        "green",
        4
    )

    # 2ª melhor
    desenhar_seta(
        segunda_jogada,
        "blue",
        4
    )

    # 1ª melhor
    desenhar_seta(
        melhor_jogada,
        "red",
        6
    )


def fazer_jogada():

    global casa_selecionada
    global melhor_jogada
    global segunda_jogada
    global terceira_jogada

    movimento = entrada.get()

    try:

        # Só permite usar o campo para o adversário
        if tabuleiro.turn == minha_cor:

            resultado.config(
                text="Agora é sua vez!"
            )

            return

        tabuleiro.push_san(movimento)

        casa_selecionada = None

        # Apaga as setas antigas
        melhor_jogada = None
        segunda_jogada = None
        terceira_jogada = None

        desenhar_tabuleiro()

        entrada.delete(0, tk.END)

        atualizar_turno()

        resultado.config(
            text="Jogada do adversário registrada!"
        )

    except:

        resultado.config(
            text="Jogada inválida!"
        )


def analisar():

    global melhor_jogada
    global segunda_jogada
    global terceira_jogada

    # Só podemos analisar quando for nossa vez
    if tabuleiro.turn != minha_cor:

        resultado.config(
            text="Espere o adversário jogar!"
        )

        return

    resultado.config(
        text="Analisando..."
    )

    janela.update()

    resultados = engine.analyse(
        tabuleiro,
        chess.engine.Limit(time=2.0),
        multipv=3
    )

    texto = ""

    # Limpa análises anteriores
    melhor_jogada = None
    segunda_jogada = None
    terceira_jogada = None

    for i, analise in enumerate(resultados):

        jogada = analise["pv"][0]

        nome_jogada = tabuleiro.san(jogada)

        avaliacao = analise["score"].pov(minha_cor).score(
            mate_score=100000
        )

        avaliacao = avaliacao / 100

        texto += (
            str(i + 1)
            + " - "
            + nome_jogada
            + " | Avaliação: "
            + str(avaliacao)
            + "\n"
        )

        # Guarda cada uma das três jogadas
        if i == 0:

            melhor_jogada = jogada

        elif i == 1:

            segunda_jogada = jogada

        elif i == 2:

            terceira_jogada = jogada

    # Redesenha para mostrar as três setas
    desenhar_tabuleiro()

    resultado.config(
        text=texto
    )


def fazer_melhor_jogada():

    global melhor_jogada
    global segunda_jogada
    global terceira_jogada
    global casa_selecionada

    # Verifica se é nossa vez
    if tabuleiro.turn != minha_cor:

        resultado.config(
            text="Agora é a vez do adversário!"
        )

        return

    # Verifica se já existe uma análise
    if melhor_jogada is None:

        resultado.config(
            text="Primeiro clique em Analisar!"
        )

        return

    try:

        tabuleiro.push(melhor_jogada)

        melhor_jogada = None
        segunda_jogada = None
        terceira_jogada = None

        casa_selecionada = None

        desenhar_tabuleiro()

        atualizar_turno()

        resultado.config(
            text="Sua melhor jogada foi realizada!"
        )

    except:

        resultado.config(
            text="Não foi possível realizar a jogada."
        )


def desenhar_coordenadas():

    letras = ["a", "b", "c", "d", "e", "f", "g", "h"]

    # Tabuleiro de brancas
    if minha_cor == chess.WHITE:

        # Letras na parte de baixo
        for coluna in range(8):

            x = margem + coluna * tamanho + tamanho / 2

            canvas.create_text(
                x,
                tamanho_tabuleiro + 12,
                text=letras[coluna],
                font=("Arial", 12)
            )

        # Números na lateral esquerda
        for linha in range(8):

            y = linha * tamanho + tamanho / 2

            numero = 8 - linha

            canvas.create_text(
                12,
                y,
                text=str(numero),
                font=("Arial", 12)
            )

    # Tabuleiro de pretas
    else:

        # Letras na parte de baixo
        for coluna in range(8):

            x = margem + coluna * tamanho + tamanho / 2

            canvas.create_text(
                x,
                tamanho_tabuleiro + 12,
                text=letras[7 - coluna],
                font=("Arial", 12)
            )

        # Números na lateral esquerda
        for linha in range(8):

            y = linha * tamanho + tamanho / 2

            numero = linha + 1

            canvas.create_text(
                12,
                y,
                text=str(numero),
                font=("Arial", 12)
            )


def desenhar_tabuleiro():

    canvas.delete("all")

    # Desenha as casas
    for linha in range(8):
        for coluna in range(8):

            x1 = margem + coluna * tamanho
            y1 = linha * tamanho
            x2 = x1 + tamanho
            y2 = y1 + tamanho

            if (linha + coluna) % 2 == 0:
                cor = "#F0D9B5"

            else:
                cor = "#B58863"

            canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=cor
            )

    # Símbolos das peças
    pecas = {
        "P": "♙",
        "N": "♘",
        "B": "♗",
        "R": "♖",
        "Q": "♕",
        "K": "♔",

        "p": "♟",
        "n": "♞",
        "b": "♝",
        "r": "♜",
        "q": "♛",
        "k": "♚"
    }

    # Desenha as peças
    for casa in chess.SQUARES:

        peca = tabuleiro.piece_at(casa)

        if peca is None:
            continue

        coluna, linha = obter_posicao_visual(casa)

        x = margem + coluna * tamanho + tamanho / 2
        y = linha * tamanho + tamanho / 2

        simbolo = pecas[peca.symbol()]

        canvas.create_text(
            x,
            y,
            text=simbolo,
            font=("Arial", 45)
        )

    # Desenha as três setas
    desenhar_setas_melhores_jogadas()

    # Desenha as coordenadas por último
    desenhar_coordenadas()


# Clique no tabuleiro
canvas.bind(
    "<Button-1>",
    clicar_tabuleiro
)


# Escolha de cor
texto_cor = tk.Label(
    janela,
    text="Você joga de: Brancas",
    font=("Arial", 14)
)

texto_cor.pack(pady=5)


botao_brancas = tk.Button(
    janela,
    text="Brancas",
    command=lambda: escolher_cor(chess.WHITE)
)

botao_brancas.pack()


botao_pretas = tk.Button(
    janela,
    text="Pretas",
    command=lambda: escolher_cor(chess.BLACK)
)

botao_pretas.pack()


# Mostra de quem é a vez
texto_turno = tk.Label(
    janela,
    text="Sua vez",
    font=("Arial", 14)
)

texto_turno.pack(pady=5)


# Campo para digitar a jogada do adversário
entrada = tk.Entry(janela)

entrada.pack(pady=10)


# Botão para registrar a jogada
botao_jogada = tk.Button(
    janela,
    text="Registrar jogada do adversário",
    command=fazer_jogada
)

botao_jogada.pack()


# Botão para analisar
botao_analisar = tk.Button(
    janela,
    text="Analisar",
    command=analisar
)

botao_analisar.pack(pady=5)


# Botão para fazer a melhor jogada
botao_melhor = tk.Button(
    janela,
    text="Fazer melhor jogada",
    command=fazer_melhor_jogada
)

botao_melhor.pack()


# Texto onde aparece o resultado
resultado = tk.Label(
    janela,
    text="",
    font=("Arial", 14)
)

resultado.pack(pady=10)


# Desenha o tabuleiro inicialmente
desenhar_tabuleiro()

atualizar_turno()


# Fecha o Stockfish quando fechar
def fechar():

    engine.quit()
    janela.destroy()


janela.protocol(
    "WM_DELETE_WINDOW",
    fechar
)


janela.mainloop()