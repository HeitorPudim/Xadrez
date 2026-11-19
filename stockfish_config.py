"""
Módulo para localizar o executável do Stockfish de forma robusta.

Funciona em qualquer pasta do repositório e suporta Windows, Linux e macOS.
Também permite sobrescrever o caminho via variável de ambiente STOCKFISH_PATH.
"""

import os
import sys


def encontrar_stockfish():
    """
    Localiza o executável do Stockfish na pasta do projeto.

    Ordem de busca:
    1. Variável de ambiente STOCKFISH_PATH (para sobrescrever)
    2. Pasta stockfish/ relativa ao diretório do projeto
    3. Possíveis nomes de executável por sistema operacional

    Returns:
        str: Caminho completo para o executável do Stockfish

    Raises:
        FileNotFoundError: Se o executável não for encontrado
    """
    # 1. Verifica variável de ambiente
    caminho_ambiente = os.environ.get("STOCKFISH_PATH")
    if caminho_ambiente and os.path.isfile(caminho_ambiente):
        return caminho_ambiente

    # 2. Caminho relativo à pasta do projeto
    diretorio_projeto = os.path.dirname(os.path.abspath(__file__))
    pasta_stockfish = os.path.join(diretorio_projeto, "stockfish")

    # 3. Possíveis nomes do executável por sistema
    if sys.platform.startswith("win"):
        # Windows: procura .exe
        nomes_possiveis = [
            "stockfish-windows-x86-64-avx2.exe",
            "stockfish-windows-x86-64-sse41-popcnt.exe",
            "stockfish-windows-x86-64-modern.exe",
            "stockfish-windows-x86-64-universal.exe",
            "stockfish.exe",
        ]
    elif sys.platform.startswith("linux"):
        # Linux
        nomes_possiveis = [
            "stockfish-linux-x86-64-avx2",
            "stockfish-linux-x86-64-sse41-popcnt",
            "stockfish-linux-x86-64-modern",
            "stockfish-linux-x86-64-universal",
            "stockfish",
        ]
    elif sys.platform == "darwin":
        # macOS
        nomes_possiveis = [
            "stockfish-mac-x86-64-avx2",
            "stockfish-mac-arm64",
            "stockfish-mac-universal",
            "stockfish",
        ]
    else:
        # Outros sistemas: tenta apenas "stockfish"
        nomes_possiveis = ["stockfish"]

    # Procura na pasta stockfish/
    for nome in nomes_possiveis:
        caminho_completo = os.path.join(pasta_stockfish, nome)
        if os.path.isfile(caminho_completo):
            return caminho_completo

    # 4. Último recurso: procura no PATH do sistema
    for nome in nomes_possiveis:
        for diretorio in os.environ.get("PATH", "").split(os.pathsep):
            caminho_completo = os.path.join(diretorio, nome)
            if os.path.isfile(caminho_completo):
                return caminho_completo

    # Não encontrou nada
    raise FileNotFoundError(
        "Executável do Stockfish não encontrado!\n"
        "Baixe em: https://github.com/official-stockfish/Stockfish/releases\n"
        "E coloque na pasta stockfish/ do projeto.\n"
        "Ou defina a variável de ambiente STOCKFISH_PATH com o caminho completo."
    )


# Caminho resolvido no momento da importação
caminho_stockfish = encontrar_stockfish()