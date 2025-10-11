import time
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'Sistema'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Algoritimo'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Simulacao'))

from Sistema.CarregadorDeTexto import CarregadorDeTexto
from Algoritimo.FIFO import FIFO
from Algoritimo.LRU import LRU
from Algoritimo.LFU import LFU
from Simulacao.Simulador import Simulador

mapa = {"FIFO": FIFO, "LRU": LRU, "LFU": LFU}
ARQ_Escolhido="algoritmo_escolhido.txt"

def inicializar_sistema():
    try:
        if not os.path.exists("Textos"):
            raise Exception("Textos não encontrados.")
        
        
        carregador = CarregadorDeTexto("Textos/")
        faltando = [i for i in range(1,50) if not os.path.exists(os.path.join("Textos",f"texto{i}.txt"))]
        if faltando:
            raise Exception(f"Faltam {len(faltando)} arquivos de texto")
        simulador = Simulador()
        escolhido = "FIFO"
        if os.path.exists(ARQ_Escolhido):
            with open(ARQ_Escolhido, encoding="utf-8") as f:
                escolhido = f.read().strip()
        
        algoritimo_cache = mapa.get(escolhido, FIFO)()
        print(f"Algoritimo de cache escolhido: {escolhido}")
        return carregador, algoritimo_cache, simulador
    
    except Exception as e:
            print(f"Erro na inicialização: {e}")
            sys.exit(1)

def mostrar_texto(texto, numero_texto, inicio):
    print(f"\n" + "="*40)
    print(f"Texto {numero_texto}")
    print("="*40)
    if texto is None:
        print("Arquivo não existe.")
    else:
        print(texto)
    print("="*40 + "\n")
    tempo = time.time() - inicio
    print(f"Tempo total: {tempo:.4f} segundos")
    input("Pressione Enter para continuar...")

def interface():
    while True:
        entrada=input("Digite o número do texto (1-100), -1 para modo simulação, 0 para sair: ")
            
        if entrada == "0":
            print("Saindo...")
            sys.exit()
        elif entrada == "-1":
            print("Modo simulação ativado.")
            return -1
        else:
            try:
                numero = int(entrada)
                if 1 <= numero <= 100:
                    return numero
                else:
                    print("Número inválido. Digite um número entre 1 e 100, -1 para modo simulação, ou 0 para sair.")
            except ValueError:
                print("Entrada inválida. Digite um número entre 1 e 100, -1 para modo simulação, ou 0 para sair.")
def main():
    print("Sistema biblioteca - Textos")

    carregador, algoritimo_cache, simulador = inicializar_sistema()

    while True:
        opcao = interface()
        if opcao == -1:
            print("Iniciando modo simulação...")
            time.sleep(1)
            vencedor=simulador.executar()
            algoritimo_cache=mapa.get(vencedor, FIFO)()
            print(f"Cache ativo alterado para : {vencedor}")
        else:
            numero_texto = opcao
            inicio = time.time()
            texto = algoritimo_cache.buscar_texto(numero_texto)
            if texto is not None:
                print(f"Texto {numero_texto} encontrado no cache")
                mostrar_texto(texto, numero_texto, inicio)
            else:
                conteudo = carregador.carregar_texto(numero_texto)
                if conteudo is not None:
                    print(f"Texto {numero_texto} carregado do disco")
                    algoritimo_cache.adicionar_texto(numero_texto, conteudo)
                else:
                    print(f"Texto {numero_texto} Não encontrado no disco")

                mostrar_texto(conteudo, numero_texto, inicio)

if __name__ == "__main__":
    main()
    