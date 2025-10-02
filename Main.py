import time
import os
import sys
from Sistema.CarregadorDeTexto import CarregadorDeTexto
from Sistema.Cache import Cache
from Algoritimo.FIFO import FIFO
from Algoritimo.LRU import LRU
from Algoritimo.LFU import LFU
from Simulacao.Simulador import Simulador
from Simulacao.Metrica import Metrica
from Simulacao.Probabilidade import Probabilidade

def inicializar_sistema():
    try:
        if not os.path.exists("Textos"):
            raise Exception("Textos não encontrados.")
        
        
        carregador = CarregadorDeTexto("Textos/")
        algoritimo_cache = FIFO()
        simulador = Simulador()
        return carregador, algoritimo_cache, simulador
    
    except Exception as e:
            print(f"Erro na inicialização: {e}")
            sys.exit(1)

def mostrar_texto(texto, numero_texto, tempo):
    print(f"\n" + "="*40)
    print(f"Texto {numero_texto} - {tempo:.4f} segundos")
    print("="*40)
    print(texto)
    print("="*40 + "\n")
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
            time.sleep(2)
            simulador.executar()
        else:
            numero_texto = opcao
            inicio = time.time()
            texto = algoritimo_cache.buscar_texto(numero_texto)
            if texto:
                tempo = time.time() - inicio
                print(f"Texto {numero_texto} encontrado no cache")
                mostrar_texto(texto, numero_texto, tempo)
            else:
                texto = carregador.carregar_texto(numero_texto)
                algoritimo_cache.adicionar_texto(numero_texto, texto)
                tempo = time.time() - inicio
                print(f"Texto {numero_texto} carregado do disco")
                mostrar_texto(texto, numero_texto, tempo)

if __name__ == "__main__":
    main()