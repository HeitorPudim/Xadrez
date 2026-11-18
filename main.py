import chess
import chess.engine

caminho_stockfish = r"C:\Users\heito\OneDrive\Documentos\xadrez_ia\stockfish\stockfish-windows-x86-64-universal"

tabuleiro = chess.Board()

engine = chess.engine.SimpleEngine.popen_uci(caminho_stockfish)

engine.configure({
    "Threads": 4,
    "Hash": 512
})

cor = input("Você joga de (b)rancas ou (p)retas? ").lower()

if cor == "b":
    minha_cor = chess.WHITE
else:
    minha_cor = chess.BLACK


while not tabuleiro.is_game_over():

    print()
    print(tabuleiro)

    # É a vez do adversário
    if tabuleiro.turn != minha_cor:

        movimento = input("\nJogada do adversário: ")

        try:
            tabuleiro.push_san(movimento)
        except:
            print("Jogada inválida!")
            continue

    # É a nossa vez
    else:

        resultados = engine.analyse(
            tabuleiro,
            chess.engine.Limit(time=3.0),
            multipv=3
        )

        print()

        for i, resultado in enumerate(resultados):

            jogada = resultado["pv"][0]

            avaliacao = resultado["score"].pov(minha_cor).score(
                mate_score=100000
            )

            print(i + 1, "-", tabuleiro.san(jogada), "| Avaliação:", avaliacao / 100)

            temp_tabuleiro = tabuleiro.copy()

            linha = []

            for movimento in resultado["pv"][:5]:
                linha.append(temp_tabuleiro.san(movimento))
                temp_tabuleiro.push(movimento)

            print("   Linha:", " ".join(linha))


        melhor_jogada = resultados[0]["pv"][0]

        tabuleiro.push(melhor_jogada)


engine.quit()