from abc import ABC, abstractmethod

class Cache(ABC):
    def __init__(self, cap=10):
        self.cap = cap
        self.cache = {}
        self.hits = 0
        self.misses = 0
    
    @abstractmethod
    def buscar_texto(self, numero_texto):
        pass
    
    @abstractmethod
    def adicionar_texto(self, numero_texto, texto):
        pass


    def stats(self):
        total = self.hits + self.misses
        taxa = (self.hits / total * 100) if total > 0 else 0
        return {
            'hits': self.hits,
            'misses': self.misses,
            'total': total,
            'taxa_hit': f'{taxa:.1f}%',
            'capacidade': self.cap
        }
    