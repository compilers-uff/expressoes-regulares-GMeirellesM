from AFNe import AFNe
from AFN import AFN
from AFD import AFD

import string

alfabeto = list(string.ascii_letters) + list(string.digits)

#### ER para AFNe ####

def criaAFNe(termo):
    delta = {'q0': [(termo, {'qf'})]}
    afne = AFNe({termo}, {'q0', 'qf'}, delta, 'q0', {'qf'})

    return afne

def atualizaAFNe(val, afne):
    ests = afne.estados
    ests = set(
        map(lambda e: e + val, ests)
    )

    delta = afne.delta
    delta = dict(
        map(lambda k: (
            k[0] + val,
            concatValorTransicoes(val, k[1])),
            delta.items())
        )

    estadoInicial = afne.estadoInicial + val
    estadosFinais = afne.estadosFinais
    estadosFinais = set(
        map(lambda e: e + val, estadosFinais)
    )

    return AFNe(afne.sigma, ests, delta, estadoInicial, estadosFinais)


def concatValorTransicoes(val, trans):
    resultado = []

    for t in trans:
        resultado.append(
            (t[0], set(
                map(lambda e: e + val, t[1])))
        )

    return resultado


def erToAFNe(er):
    er = er.replace(' ', '').replace('(', '').replace(')', '').replace(',', '').replace('\'', '').replace('\"', '')[::-1]

    auxiliar = []

    while len(er) > 0:

        c = er[0]
        er = er[1:]

        if c in alfabeto:
            auxiliar.append(c)
        else:
            primTermo = auxiliar.pop()

            if primTermo in alfabeto:
                primTermo = criaAFNe(primTermo)

            primTermo_novo = atualizaAFNe('1', primTermo)

            segTermo = None
            segTermo_novo = None
            sigma = None

            if c != "*":
                segTermo = auxiliar.pop()

                if segTermo in alfabeto:
                    segTermo = criaAFNe(segTermo)

                segTermo_novo = atualizaAFNe('2', segTermo)
                sigma = primTermo_novo.sigma.union(segTermo_novo.sigma)
            else:
                sigma = primTermo_novo.sigma.copy()

            if c == '.':

                ests = primTermo_novo.estados.union(segTermo_novo.estados)

                delta = {list(primTermo_novo.estadosFinais)[0]: [
                    (None, {segTermo_novo.estadoInicial})
                    ]}

                delta.update(primTermo_novo.delta)
                delta.update(segTermo_novo.delta)
                estadoInicial = primTermo_novo.estadoInicial

                estadosFinais = {list(segTermo_novo.estadosFinais)[0]}

                resultadoAFNe = AFNe(sigma, ests, delta, estadoInicial, estadosFinais)

                auxiliar.append(resultadoAFNe)

            elif c == '+':
                ests = primTermo_novo.estados.union(segTermo_novo.estados)
                ests.add('q0')
                ests.add('qf')

                delta = {
                    'q0': [(None, {primTermo_novo.estadoInicial}), (None, {segTermo_novo.estadoInicial})],
                    list(primTermo_novo.estadosFinais)[0]: [(None, {'qf'})],
                    list(segTermo_novo.estadosFinais)[0]: [(None, {'qf'})]
                }

                delta.update(primTermo_novo.delta)
                delta.update(segTermo_novo.delta)

                estadoInicial = 'q0'
                estadosFinais = {'qf'}

                resultadoAFNe = AFNe(sigma, ests, delta, estadoInicial, estadosFinais)

                auxiliar.append(resultadoAFNe)

            elif c == '*':

                ests = primTermo_novo.estados
                ests.add('q0')
                ests.add('qf')

                delta = {
                    'q0': [(None, {'qf'}), (None, {primTermo_novo.estadoInicial})],
                    list(primTermo_novo.estadosFinais)[0]: [(None, {primTermo_novo.estadoInicial}), (None, {'qf'})],
                }

                delta.update(primTermo_novo.delta)

                estadoInicial = 'q0'
                estadosFinais = {'qf'}

                resultadoAFNe = AFNe(sigma, ests, delta, estadoInicial, estadosFinais)

                auxiliar.append(resultadoAFNe)

    ultElem = auxiliar.pop()
    invalidElems = {'+', '.', '*'}

    if ultElem in invalidElems:
        exit("Contém elementos inválidos")

    if ultElem in alfabeto:
        ultElem = criaAFNe(ultElem)

    return ultElem


#### AFNe para AFN ####

def afneToAFN(afne):
    sigma = afne.sigma.copy()
    ests = afne.estados.copy()
    delta = {}
    estadoInicial = afne.estadoInicial
    estadosFinais = set()

    for e in ests:
        estsAlcancados = afne.fecho_vazio(e)

        if not estsAlcancados.isdisjoint(afne.estadosFinais):
            estadosFinais.add(e)

        for c in sigma:
            resp = afne.delta_estr({e}, c)
            ##AQUI
            if len(resp) != 0:
                if e in delta:
                    delta[e].append((c, resp))
                else:
                    delta[e] = [(c, resp)]

    afn = AFN(sigma, ests, delta, estadoInicial, estadosFinais)

    return afn

#### AFN para AFD ####

def afnToAFD(afn):
    sigma = afn.sigma.copy()
    ests = set()
    delta = {}
    estadoInicial = None
    estadosFinais = set()

    finais = []
    iniciais = [{afn.estadoInicial}]

    trans = []

    while len(iniciais) > 0:
        e = iniciais.pop(0)
        finais.append(e)

        for c in sigma:
            resp = afn.delta_estr(e, c)
            if len(resp) > 0:
                trans.append([e.copy(), c, resp])
                if resp not in finais:
                    iniciais.append(resp)

    cont = 0
    for t in trans:
        est = t[0]
        des = t[2]

        if isinstance(est, set):
            ests.add('q' + str(cont))

            if not est.isdisjoint(afn.estadosFinais):
                estadosFinais.add('q' + str(cont))

            if list(est)[0] == afn.estadoInicial and estadoInicial == None:
                estadoInicial = 'q' + str(cont)

            for tr in trans:
                if tr[0] == est:
                    tr[0] = 'q' + str(cont)
                if tr[2] == est:
                    tr[2] = 'q' + str(cont)

            cont = cont + 1

        if est != des:
            if isinstance(des, set):

                ests.add('q' + str(cont))

                if not des.isdisjoint(afn.estadosFinais):
                    estadosFinais.add('q' + str(cont))

                if list(des)[0] == afn.estadoInicial and estadoInicial == None:
                    estadoInicial = 'q' + str(cont)

                for tr in trans:
                    if tr[0] == des:
                        tr[0] = 'q' + str(cont)
                    if tr[2] == des:
                        tr[2] = 'q' + str(cont)
                cont = cont + 1

    for t in trans:
        est = t[0]
        termo = t[1]
        des = t[2]

        if est not in delta:
            delta[est] = [(termo, {des})]
        else:
            delta[est].append((termo, {des}))

    afd = AFD(sigma, ests, delta, estadoInicial, estadosFinais)

    return afd

#### AFD para AFDmin ####

def retiraEstadosInalcancaveis(afd):

    checados = set()
    check = [afd.estadoInicial]

    while len(check) > 0:
        est = check.pop(0)
        checados.add(est)

        if est in afd.delta:
            for t in afd.delta[est]:
                if list(t[1])[0] not in checados:
                    check.append(list(t[1])[0])

    estsInalcancaveis = afd.estados - checados
    afd.estados = afd.estados - estsInalcancaveis
    afd.estadosFinais = afd.estadosFinais - estsInalcancaveis

    for e in estsInalcancaveis:
        if e in afd.delta:
            del afd.delta[e]


def totalDelta(afd):
    check = False
    d = 'd'
    ##AQUI
    while d in afd.estados:
        d = d + 'd'

    estadosEncontrados = set()
    for e in afd.delta:
        estadosEncontrados.add(e)
        transEncontradas = set()
        for t in afd.delta[e]:
            transEncontradas.add(t[0])

        if transEncontradas != afd.sigma:
            if not check:
                check = True
                afd.estados.add(d)
            adicionaTrans = afd.sigma - transEncontradas
            for c in adicionaTrans:
                afd.delta[e].append((c, {d}))
    adicionaEstados = afd.estados - estadosEncontrados
    if len(adicionaEstados) > 0:
        if not check:
            check = True
            afd.estados.add(d)
            adicionaEstados.add(d)

        for e in adicionaEstados:
            afd.delta[e] = []
            for c in afd.sigma:
                afd.delta[e].append((c, {d}))


def criaTabela(afd):
    tab = {}
    ests = list(afd.estados)

    for e in ests:
        tab[e] = {}
        for es in ests:
            if es != e:
                if es in afd.estadosFinais and e not in afd.estadosFinais:
                    tab[e][es] = False
                elif es not in afd.estadosFinais and e in afd.estadosFinais:
                    tab[e][es] = False
                else:
                    tab[e][es] = True
    return tab


def fechaLista(lista, tab, ests):
    for i in lista:
        if i[0] == ests:
            for j in range(1, len(i)):
                if tab[list(i[j])[0]][list(i[j])[1]]:
                    tab[list(i[j])[0]][list(i[j])[1]] = False
                    tab[list(i[j])[1]][list(i[j])[0]] = False
                    fechaLista(lista, tab, i[j])


def adicionaLista(ests1, ests2, lista):
    inicia = False
    chave = None

    for i, j in enumerate(lista):
        if j[0] == ests1:
            inicia = True
            chave = i

    if inicia:
        lista[chave].append(ests2)
    else:
        lista.append([ests1, ests2])


def encontraEquivalentes(afd, tab):
    ests = list(afd.estados)
    depLista = []
    checados = []

    for e in ests:
        for es in ests:
            if es != e and tab[e][es] and {e, es} not in checados:
                checados.append({e, es})
                for c in afd.sigma:
                    res1 = list(afd.delta_estr({e}, c))[0]
                    res2 = list(afd.delta_estr({es}, c))[0]
                    if res1 != res2:
                        if not tab[res1][res2]:
                            tab[e][es] = False
                            tab[es][e] = False
                            fechaLista(depLista, tab, {e, es})
                            break
                        else:
                            adicionaLista({res1, res2}, {e, es}, depLista)


def equivalenciaEstTrans(tab, est):
    res = set()
    res.add(est)

    inicial = [est]
    finais = []

    while len(inicial) > 0:
        e = inicial.pop(0)
        finais.append(e)
        for i in tab[e]:
            if tab[e][i]:
                res.add(i)
                if i not in finais:
                    inicial.append(i)

    return res


def retiraEstadosInuteis(afd):

    estsInuteis = set()

    for e in afd.estados:
        checados = set()
        check = [e]

        while len(check) > 0:
            est = check.pop(0)
            checados.add(est)

            if est in afd.delta:
                for t in afd.delta[est]:
                    if list(t[1])[0] not in checados:
                        check.append(list(t[1])[0])

        if checados.isdisjoint(afd.estadosFinais):
            estsInuteis.add(e)

    afd.estados = afd.estados - estsInuteis
    afd.estadosFinais = afd.estadosFinais - estsInuteis

    for e in estsInuteis:
        if e in afd.delta:
            del afd.delta[e]

    transInuteis = []
    for e in afd.delta:
        trans_novas = []
        for t in afd.delta[e]:
            if list(t[1])[0] not in estsInuteis:
                trans_novas.append(t)
                ##AQUI
        if len(trans_novas) < 1:
            transInuteis.append(e)

        afd.delta[e] = trans_novas

    for e in transInuteis:
        del afd.delta[e]










def afdToAFDmin(afd):
    if not isinstance(afd, AFD):
        raise Exception("O automato inserido é nao-deterministico")

    afdmin = AFD(afd.sigma.copy(), afd.estados.copy(), afd.delta.copy(), afd.estadoInicial, afd.estadosFinais.copy())

    retiraEstadosInalcancaveis(afdmin)
    totalDelta(afdmin)
    tab = criaTabela(afdmin)
    encontraEquivalentes(afdmin, tab)

    resultado = []
    estsUnificados = []

    for e in tab:
        finais = False
        for conjs in resultado:
            if e in conjs:
                finais = True
                break

        if not finais:
            resultado.append(equivalenciaEstTrans(tab, e))

    for i in range(len(resultado)):
        estsUnificados.append('q' + str(i))

    afdmin.estados = set(estsUnificados)

    deltaRes = {}
    trans = []

    for e in afdmin.delta:
        for t in afdmin.delta[e]:
            trans.append([e, t[0], t[1]])

    for t in trans:
        comeco = t[0]
        comecoTransformado = None
        des = list(t[2])[0]
        desTransformado = None

        for ind, conj in enumerate(resultado):
            if comeco in conj:
                comecoTransformado = estsUnificados[ind]
            if des in conj:
                desTransformado = estsUnificados[ind]

        t[0] = comecoTransformado
        t[2] = {desTransformado}

    for t in trans:
        if t[0] not in deltaRes:
            deltaRes[t[0]] = []
        if (t[1], t[2]) not in deltaRes[t[0]]:
            deltaRes[t[0]].append((t[1], t[2]))

    estInicialRes = None
    estsFinaisRes = set()

    for ind, conj in enumerate(resultado):
        for e in conj:
            if e in afdmin.estadosFinais:
                estsFinaisRes.add(estsUnificados[ind])
            if e == afdmin.estadoInicial:
                estInicialRes = estsUnificados[ind]

    afdmin.estadoInicial = estInicialRes
    afdmin.estadosFinais = estsFinaisRes
    afdmin.delta = deltaRes

    retiraEstadosInuteis(afdmin)

    return afdmin

def match(er, palavra):

    return afdToAFDmin(afnToAFD(afneToAFN(erToAFNe(er)))).accepted(palavra)





