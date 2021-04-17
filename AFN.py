import Automato


class AFN(Automato.Automato):

    def __init__(self, sigma, estados, delta, estadoInicial, estadosFinais):

        for i, j in enumerate(delta):
            for t in delta[j]:
                if t[0] == None:
                    raise ValueError("Indeterminismo")

        super().__init__(sigma, estados, delta, estadoInicial, estadosFinais)



    def delta_estr(self, estados, palavra):

        if palavra == None or palavra == '':
            return estados

        primLetra = None
        restoPalavra = None

        primLetra = palavra[0]
        restoPalavra = palavra[1:]

        if restoPalavra == '':
            restoPalavra = None

        a = set()

        for e in estados:
            if e not in self.estados:
                raise Exception("Estado não existente")

            if e in self.delta:
                trans = self.delta[e]
                for t in trans:
                    if t[0] == primLetra:
                        a = a.union(t[1])

        if len(a) == 0:
            return a

        return self.delta_estr(a, restoPalavra)





