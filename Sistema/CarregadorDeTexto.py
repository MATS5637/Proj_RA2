import os
import time
import random

class CarregadorDeTexto:
    def __init__(self, diretorio, verbose=False, min_palavras=1000):
        self.diretorio = diretorio
        self.verbose = verbose
        self.min_palavras = min_palavras

    def carregar_texto(self, numero_texto):
        time.sleep(random.uniform(0.01, 0.1))

        caminho_arquivo = os.path.join(self.diretorio, f"texto{numero_texto}.txt")
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                conteudo = arquivo.read()
        except FileNotFoundError:
            if self.verbose:
                print(f"Arquivo {caminho_arquivo} não encontrado.")
            return None
        except Exception as e:
            if self.verbose:
                print(f"Erro ao carregar {caminho_arquivo}: {e}")
            return None
    
        if len(conteudo.split()) < self.min_palavras:
            if self.verbose:
                print(f"Arquivo {caminho_arquivo} tem menos de {self.min_palavras} palavras.")
            return None
        return conteudo 
        