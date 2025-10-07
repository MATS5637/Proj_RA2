from collections import defaultdict

class Metrica:
    def __init__(self, algoritimo):
        self.algoritimo = algoritimo
        self.hits = 0
        self.misses = 0
        self.t_disco = []
        self.t_cache = []
        self.misses_texto = defaultdict(int)

    def registro_hit(self, tempo):
        self.hits += 1
        self.t_cache.append(tempo)

    def registro_miss(self, tempo, numero_texto):
        self.misses += 1
        self.t_disco.append(tempo)
        self.misses_texto[numero_texto] += 1

    def total_acessos(self):
        return self.hits + self.misses
    
    def taxa_hit(self):
        return (self.hits / self.total_acessos() * 100) if self.total_acessos() > 0 else 0
    
    def taxa_miss(self):
        return (self.misses / self.total_acessos() * 100) if self.total_acessos() > 0 else 0
    
    def tempo_medio_cache(self):
        return (sum(self.t_cache) / len(self.t_cache)) if self.t_cache else 0
    
    def tempo_medio_disco(self):
        return (sum(self.t_disco) / len(self.t_disco)) if self.t_disco else 0
    
    def tempo_medio_total(self):
        todos_tempos = self.t_cache + self.t_disco
        return (sum(todos_tempos) / len(todos_tempos)) if todos_tempos else 0
    
    def texto_mais_miss(self):
        if not self.misses_texto:
            return None, 0
        texto, count = max(self.misses_texto.items(), key=lambda item: item[1])
        return texto, count
    
    def relatorio(self):
        texto_mais_miss, count = self.texto_mais_miss()
        relatorio = {
            "Algoritmo": self.algoritimo.__class__.__name__,
            "Total de Acessos": self.total_acessos(),
            "Hits": self.hits,
            "Misses": self.misses,
            "Taxa de Hit (%)": self.taxa_hit(),
            "Taxa de Miss (%)": self.taxa_miss(),
            "Tempo Médio Cache (s)": self.tempo_medio_cache(),
            "Tempo Médio Disco (s)": self.tempo_medio_disco(),
            "Tempo Médio Total (s)": self.tempo_medio_total(),
            "Texto com mais Misses": texto_mais_miss,
            "Número de Misses do Texto": count
        }
        return relatorio
    