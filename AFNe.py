from Automato import *


class AFNe(Automato):

    def __init__(self, sigma, estados, delta, estadoInicial, estadosFinais):
        super().__init__(sigma, estados, delta, estadoInicial, estadosFinais)




    def delta_estr(self, estados, palavra):

        if palavra == None:
            a = set()
            for e in estados:
                a = a.union(self.fecho_vazio(e))

            return a

        auxiliar1 = None
        auxiliar2 = None

        if palavra[:-1] != '':
            auxiliar1 = palavra[:-1]

        auxiliar2 = palavra[-1]

        conj1 = self.delta_estr(estados, auxiliar1)
        conj2 = set()

        for i in conj1:
            if i in self.delta:
                alcancaveis = self.delta[i]
                for j in alcancaveis:
                    if j[0] == auxiliar2:
                        conj2 = conj2.union(j[1])

        a = set()

        for t in conj2:
            a = a.union(self.fecho_vazio(t))

        return a


    def fecho_vazio(self, estado):

        a = set()
        inicial = [estado]
        final = set()

        while len(inicial) > 0:
            auxiliar = inicial[0]
            a.add(auxiliar)

            if auxiliar in self.delta:
                estadosAlcancaveis = self.delta[auxiliar]

                for estadoAlcancavel in estadosAlcancaveis:
                    if estadoAlcancavel[0] == None:
                        if final == set():
                            for i in estadoAlcancavel[1]:
                                inicial.append(i)
                        else:
                            for i in estadoAlcancavel[1]:
                                if i not in final:
                                    inicial.append(i)

            inicial.remove(auxiliar)
            final.add(auxiliar)

        return a