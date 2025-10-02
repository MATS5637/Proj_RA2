import time
import matplotlib.pyplot as plt
from Algoritimo.FIFO import FIFO
from Algoritimo.LRU import LRU
from Algoritimo.LFU import LFU
from Sistema.CarregadorDeTexto import CarregadorDeTexto
from Simulacao.Metrica import Metrica
from Simulacao.Probabilidade import Probabilidade

class Simulador:
    def __init__(self):
        self.carregador = CarregadorDeTexto("textos/")
        self.algoritmos = {
            "FIFO": FIFO(),
            "LRU": LRU(),
            "LFU": LFU() 
        }

    def executar(self):
        print("SIMULAÇÃO")
        resultados = []

        for algoritimo_nome, algoritimo_obj in self.algoritmos.items():
            print(f"\nTestando {algoritimo_nome}...")
            for usuario in Probabilidade.gerar_usuarios(3,200):
                for tipo, solics in usuario['solicitacoes'].items():
                    m=Metrica(algoritimo_obj)
                    for texto_id in solics:
                        inicio = time.time()
                        texto = algoritimo_obj.buscar_texto(texto_id)
                        if texto:
                            m.registro_hit(time.time() - inicio)
                        else:
                            texto = self.carregador.carregar_texto(texto_id)
                            algoritimo_obj.adicionar_texto(texto_id, texto)
                            m.registro_miss(time.time() - inicio, texto_id)
                    resultados.append({"algoritimo": algoritimo_nome, "metrica": m})

        stats = {}
        for res in resultados:
            algoritimo = res["algoritimo"]
            if algoritimo not in stats:
                stats[algoritimo] = {"hits": 0, "misses": 0}
            stats[algoritimo]["hits"] += res["metrica"].hits
            stats[algoritimo]["misses"] += res["metrica"].misses

        melhor_algoritimo = None
        melhor_taxa = 0
        for algoritimo, data in stats.items():
            total = data["hits"] + data["misses"]
            taxa_hit = (data["hits"] / total * 100) if total > 0 else 0
            print(f"{algoritimo} - Hits: {data['hits']}, Misses: {data['misses']}, Taxa de Hit: {taxa_hit:.2f}%")
            if taxa_hit > melhor_taxa:
                melhor_taxa = taxa_hit
                melhor_algoritimo = algoritimo

        print(f"\nMelhor Algoritmo: {melhor_algoritimo}\n")
        return melhor_algoritimo
    
if __name__ == "__main__":
    Simulador().executar()