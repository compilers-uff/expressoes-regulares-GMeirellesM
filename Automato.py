class Automato():

    def __init__(self, sigma, estados, delta, estadoInicial, estadosFinais):
        self.sigma = sigma
        self.estados = estados
        self.delta = delta
        self.estadoInicial = estadoInicial
        self.estadosFinais = estadosFinais

    def __str__(self):
        return "Autômato: \n" + \
               "   Sigma: " + str(self.sigma) + "\n" + \
               "   Estados: " + str(self.estados) + "\n" + \
               "   Delta: " + str(self.delta) + "\n" + \
               "   Estado Inicial: " + str(self.estadoInicial) + "\n" + \
               "   Estados Finais: " + str(self.estadosFinais)
