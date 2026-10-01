class Cliente:

    def __init__(
            self,
            numero,
            servidor,
            llegada,
            servicio,
            espera,
            inicio,
            fin
    ):
        self.numero = numero
        self.servidor = servidor
        self.llegada = llegada
        self.servicio = servicio
        self.espera = espera
        self.inicio = inicio
        self.fin = fin

    def getNumero(self):
        return self.numero

    def getServidor(self):
        return self.servidor

    def getLlegada(self):
        return self.llegada

    def getServicio(self):
        return self.servicio

    def getEspera(self):
        return self.espera

    def getInicio(self):
        return self.inicio

    def getFin(self):
        return self.fin