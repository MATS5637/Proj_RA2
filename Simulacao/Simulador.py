import time
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
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
            print(f"\nResultados do algoritmo {nome}:")
            metrica_total = Metrica(ClasseAlgoritimo()) 
            cache = ClasseAlgoritimo()

            for usuario in usuarios:
                for _, solicitacoes in usuario["solicitacoes"].items():
                    metrica_cenario = Metrica(cache)

                    for texto_id in solicitacoes:
                        inicio = time.time()
                        texto = cache.buscar_texto(texto_id)

                        if texto is not None:
                            metrica_cenario.registro_hit(time.time() - inicio)
                        else:
                            texto_real = self.carregador.carregar_texto(texto_id)
                            if texto_real is not None:
                                cache.adicionar_texto(texto_id, texto_real)
                                metrica_cenario.registro_miss(time.time() - inicio, texto_id)
                            else:
                                print(f"Texto {texto_id} não encontrado no disco.")
                                continue
                    
                    metrica_total.hits += metrica_cenario.hits
                    metrica_total.misses += metrica_cenario.misses
                    metrica_total.t_cache.extend(metrica_cenario.t_cache)
                    metrica_total.t_disco.extend(metrica_cenario.t_disco)

                    for texto_id, qtd in metrica_cenario.misses_texto.items():
                        metrica_total.misses_texto[texto_id] += qtd

            resultados.append((nome, metrica_total))
            taxa = metrica_total.taxa_hit()
            print(f"   {nome}: {metrica_total.hits} hits, {metrica_total.misses} misses, Taxa de Hits: {taxa:.2f}%")

        print("\nResultados:")
        melhor_nome, melhor_taxa = None, -1.0
        for nome, m in resultados:
            taxa = m.taxa_hit()
            print(f"{nome}:")
            print(f"Hits: {m.hits}, Misses: {m.misses}, Taxa de Hits: {taxa:.2f}%")
            print(f"Tempo Médio Cache: {m.tempo_medio_cache():.4f}s, Tempo Médio Disco: {m.tempo_medio_disco():.4f}s, Tempo Médio Total: {m.tempo_medio_total():.4f}s")
            if taxa > melhor_taxa:
                melhor_nome, melhor_taxa = nome, taxa
        print(f"\nMelhor Algoritimo: {melhor_nome} ({melhor_taxa: .2f}%)")
        
        self.gerar_graficos(resultados)

        with open("algoritmo_escolhido.txt", "w", encoding="utf-8") as f:
            f.write(melhor_nome)

        return melhor_nome

    def gerar_graficos(self, resultados):
        algo_graf = [nome for nome, _m in resultados]
        taxas = [m.taxa_hit() for _, m in resultados]
        tcache = [m.tempo_medio_cache() for _, m in resultados]
        tdisco = [m.tempo_medio_disco() for _, m in resultados]
        tcache_ms= [t * 1000 for t in tcache]
        tdisco_ms= [t * 1000 for t in tdisco]
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
        plt.bar(x - w/2, tcache_ms, width=w, label='Tempo Médio Cache (ms)', alpha=0.85)
        plt.bar(x + w/2, tdisco_ms, width=w, label='Tempo Médio Disco (ms)', alpha=0.85)
        plt.xticks(x, algo_graf)
        plt.ylabel('Tempo Médio (ms)')
        plt.title('Tempo Médio por Algoritmo (Cache vs Disco)')
        plt.legend()
        plt.grid(True, axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig('comparacao_tempo_medio.png', dpi=300)
        plt.show()

        misses_totais = defaultdict(int)
        for _, m in resultados:
            for texto_id, qtd in m.misses_texto.items():
                misses_totais[texto_id] += qtd
        
        if misses_totais:
            top = sorted(misses_totais.items(), key=lambda item: item[1], reverse=True)[:10]
            labels = [f"texto {tid}" for tid, _ in top]
            valores = [q for _, q in top]

            plt.figure()
            bars3 = plt.bar(labels, valores, alpha=0.85)
            plt.ylabel('Número de Misses')
            plt.title('Top 10 Textos com Mais Misses (Todos Algoritmos)')
            for b, v in zip(bars3, valores):
                plt.text(b.get_x() + b.get_width() / 2, b.get_height()+0.5, f"{v}", ha='center', va='bottom')
            plt.xticks(rotation=30, ha='right')
            plt.grid(True, axis='y', alpha=0.3)
            plt.tight_layout()
            plt.savefig('top10_misses_textos.png', dpi=300)
            plt.show()

        print("\nGráficos gerados: ")
        print(" - comparacao_taxa_hits.png (Taxa de Hit)")
        print(" - comparacao_tempo_medio.png (Tempo Médio Cache vs Disco)")

if __name__ == "__main__":
    Simulador().executar()
