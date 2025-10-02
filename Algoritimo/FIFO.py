class FIFO:
    def __init__(self, capacidade=10):
        self.capacidade = capacidade
        self.cache = {}
        self.fila = []
        self.hits = 0
        self.misses = 0

    def buscar_texto(self, numero_texto):
        if numero_texto in self.cache:
            self.hits += 1
            return self.cache[numero_texto]
        else:
            self.misses += 1
            return None

    def adicionar_texto(self, numero_texto, texto):
        if numero_texto in self.cache:
            return  # Texto já está no cache

        if len(self.cache) >= self.capacidade:
            texto_removido = self.fila.pop(0)
            del self.cache[texto_removido]

        self.cache[numero_texto] = texto
        self.fila.append(numero_texto)
