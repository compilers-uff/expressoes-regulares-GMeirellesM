import Automato


class AFD(Automato.Automato):

    def __init__(self, sigma, estados, delta, estadoInicial, estadosFinais):

        for i, j in enumerate(delta):
            for t in delta[j]:
                if len(t[1]) > 1 or t[0] == None:
                    raise ValueError("Indeterminismo")

        super().__init__(sigma, estados, delta, estadoInicial, estadosFinais)



    def delta_estr(self, estado, palavra):

        if list(estado)[0] not in self.delta:
            return None

        if list(estado)[0] not in self.estados:
            raise Exception("Estado não existente")

        if palavra == None or palavra == '':
            return estado

        primLetra = None
        restoPalavra = None

        primLetra = palavra[0]
        restoPalavra = palavra[1:]

        if restoPalavra == '':
            restoPalavra = None

        a = None

        for t in self.delta[list(estado)[0]]:
            if t[0] == primLetra:
                a = t[1]

        if a == None:
            return None

        return self.delta_estr(a, restoPalavra)


    def accepted(self, palavra):

        estAlcancado = self.delta_estr({self.estadoInicial}, palavra)

        if estAlcancado and not estAlcancado.isdisjoint(self.estadosFinais):
            return True

        return False



