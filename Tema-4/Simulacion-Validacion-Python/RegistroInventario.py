class RegistroInventario:

    def __init__(
            self,
            periodo,
            inventarioInicial,
            demanda,
            pedido,
            inventarioFinal,
            faltante
    ):
        self.periodo = periodo
        self.inventarioInicial = inventarioInicial
        self.demanda = demanda
        self.pedido = pedido
        self.inventarioFinal = inventarioFinal
        self.faltante = faltante

    def getPeriodo(self):
        return self.periodo

    def getInventarioInicial(self):
        return self.inventarioInicial

    def getDemanda(self):
        return self.demanda

    def getPedido(self):
        return self.pedido

    def getInventarioFinal(self):
        return self.inventarioFinal

    def getFaltante(self):
        return self.faltante