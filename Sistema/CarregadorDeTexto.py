import os
import time
import random

class CarregadorDeTexto:
    def __init__(self, diretorio):
        self.diretorio = diretorio

    def carregar_texto(self, numero_texto):

        tempo_carregamento = random.uniform(0.1, 0.5)
        time.sleep(tempo_carregamento)

        caminho_arquivo = os.path.join(self.diretorio, f"texto{numero_texto}.txt")
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                return arquivo.read()
        except FileNotFoundError:
            print(f"Arquivo {caminho_arquivo} não encontrado.")
            return f"Texto {numero_texto} não encontrado."