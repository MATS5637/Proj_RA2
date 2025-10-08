import time
import matplotlib.pyplot as plt
import numpy as np
from Algoritimo.FIFO import FIFO
from Algoritimo.LRU import LRU
from Algoritimo.LFU import LFU
from Sistema.CarregadorDeTexto import CarregadorDeTexto
from Simulacao.Metrica import Metrica
from Simulacao.Probabilidade import Probabilidade

class Simulador:
    def __init__(self):
        self.carregador = CarregadorDeTexto("Textos/")
    
    def executar(self):
        usuarios = Probabilidade.gerar_usuarios(3, 200)
        algoritmos = [("FIFO", FIFO), ("LRU",LRU), ("LFU",LFU)]
        resultados = []

        for nome, ClasseAlgoritimo in algoritmos:
            metrica_total = Metrica(ClasseAlgoritimo())  

            for usuario in usuarios:
                for tipo, solicitacoes in usuario["solicitacoes"].items():
                    cache = ClasseAlgoritimo()
                    metrica_cenario = Metrica(cache)

                    for texto_id in solicitacoes:
                        inicio = time.time()
                        texto = cache.buscar_texto(texto_id)

                        if texto is not None:
                            metrica_cenario.registro_hit(time.time() - inicio)
                        else:
                            texto_real = self.carregador.carregar_texto(texto_id)
                            cache.adicionar_texto(texto_id, texto_real)
                            metrica_cenario.registro_miss(time.time() - inicio, texto_id)
                    
                    metrica_total.hits += metrica_cenario.hits
                    metrica_total.misses += metrica_cenario.misses
                    metrica_total.t_cache.extend(metrica_cenario.t_cache)
                    metrica_total.t_disco.extend(metrica_cenario.t_disco)

            resultados.append((nome, metrica_total))
            print(f"{nome} - Hits: {metrica_total.hits}, Misses: {metrica_total.misses}, "
                    f"Taxa de hits: {metrica_total.taxa_hit():.1f}%")

        melhor_nome, melhor_metrica = max(resultados, key=lambda x: x[1].taxa_hit())

        self.gerar_graficos(resultados)

        with open("algoritimo_escolhido.txt", "w") as f:
            f.write(melhor_nome)

        print(f"\nMelhor Algoritimo: {melhor_nome} ({melhor_metrica.taxa_hit():.1f}% de hits)")
        return melhor_nome

    def gerar_graficos(self, resultados):
        algo_graf = [nome for nome, _m in resultados]
        taxas = [m.taxa_hit() for _, m in resultados]
        tcache = [m.tempo_medio_cache() for _, m in resultados]
        tdisco = [m.tempo_medio_disco() for _, m in resultados]
        plt.figure()
        bars = plt.bar(algo_graf, taxas, alpha=0.85)
        plt.ylim(0, 100)
        plt.ylabel('Taxa de Hits (%)')
        plt.title('Taxa de Hits por Algoritmo')
        for b, v in zip(bars, taxas):
            plt.text(b.get_x() + b.get_width() / 2, b.get_height()+1, f"{v:.1f}%", ha='center', va='bottom')
        plt.grid(True, axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig('comparacao_taxa_hits.png', dpi=300)
        plt.show()

        x= np.arange(len(algo_graf))
        w=0.38
        plt.figure()
        plt.bar(x - w/2, tcache, width=w, label='Tempo Médio Cache (s)', alpha=0.85)
        plt.bar(x + w/2, tdisco, width=w, label='Tempo Médio Disco (s)', alpha=0.85)
        plt.xticks(x, algo_graf)
        plt.ylabel('Tempo Médio (s)')
        plt.title('Tempo Médio por Algoritmo (Cache vs Disco)')
        plt.legend()
        plt.grid(True, axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig('comparacao_tempo_medio.png', dpi=300)
        plt.show()

        print("\nGráficos gerados: ")
        print(" - comparacao_taxa_hits.png (Taxa de Hit)")
        print(" - comparacao_tempo_medio.png (Tempo Médio Cache vs Disco)")

if __name__ == "__main__":
    Simulador().executar()