from collections import defaultdict

class Metrica:
    def __init__(self, algoritimo=None, nome_algoritimo="", usuario_id=None, padrao_acesso=""):
        self.algoritimo = algoritimo
        self.nome_algoritimo = nome_algoritimo or (algoritimo.__class__.__name__ if algoritimo else "Desconhecido")
        self.usuario_id = usuario_id
        self.padrao_acesso = padrao_acesso

        self.hits = 0
        self.misses = 0
        self.t_disco = []
        self.t_cache = []

        self.misses_texto = defaultdict(int)
        self.hits_texto = defaultdict(int)
        self.tempos_por_texto = defaultdict(list)

    def registro_hit(self, tempo, numero_texto):
        self.hits += 1
        self.t_cache.append(tempo)
        self.hits_texto[numero_texto] += 1
        self.tempos_por_texto[numero_texto].append(tempo)

    def registro_miss(self, tempo, numero_texto):
        self.misses += 1
        self.t_disco.append(tempo)
        self.misses_texto[numero_texto] += 1
        self.tempos_por_texto[numero_texto].append(tempo)

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
    
    def analise_por_texto(self):
        analise = {}
        textos = set(self.hits_texto)|set(self.misses_texto) 
        for texto_id in sorted(textos):
            h = self.hits_texto.get(texto_id, 0)
            m = self.misses_texto.get(texto_id, 0)
            total = h + m
            tempos = self.tempos_por_texto.get(texto_id, [])
            tempo_medio = (sum(tempos) / len(tempos)) if tempos else 0
            analise[texto_id] = {
                "hits": h,
                "misses": m,
                "total": total,
                "taxa_hit (%)": (h / total * 100) if total > 0 else 0,
                "tempo_medio (s)": tempo_medio
            }
        return analise
    
    def relatorio(self):
        texto_mais_miss, count = self.texto_mais_miss()
        relatorio = {
            "Algoritmo": self.nome_algoritimo,
            "Usuario ID": self.usuario_id,
            "Padrão de Acesso": self.padrao_acesso,
            "Total de Acessos": self.total_acessos(),
            "Hits": self.hits,
            "Misses": self.misses,
            "Taxa de Hit (%)": self.taxa_hit(),
            "Taxa de Miss (%)": self.taxa_miss(),
            "Tempo Médio Cache (s)": round(self.tempo_medio_cache(),6),
            "Tempo Médio Disco (s)": round(self.tempo_medio_disco(),6),
            "Tempo Médio Total (s)": round(self.tempo_medio_total(),6),
            "Texto com mais Misses": texto_mais_miss,
            "Número de Misses do Texto": count
        }
        return relatorio

    def relatorio_completo(self):
        base = self.relatorio()
        base["Análise por Texto"] = self.analise_por_texto()
        base["Total de Textos Acessados"] = len(base["Análise por Texto"])
        return base
    def __str__(self):
        return(f"{self.nome_algoritimo}|Usuario{self.usuario_id}|{self.padrao_acesso}|"
               f"{self.hits} hits, {self.misses} misses "
                f"({self.taxa_hit():.2f}% hits)|")
    