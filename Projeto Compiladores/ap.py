class Pilha(object):
    def __init__(self):
        self.dados = []
#self.est = []
#self.parent = -1 
 
    def empilha(self, elemento):
        self.dados.append(elemento)
#self.est.append(num)
#self.parent = num
    def desempilha(self,tam):
        for i in range(0,tam):
            self.dados.pop(-1)
    def tam(self):
        return len(self.dados)
    def topo(self):
        return self.dados[-1]