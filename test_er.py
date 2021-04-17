import pytest
import operacoes


def test_0():
    assert operacoes.match("a", "a") == True


def test_1():
    assert operacoes.match("+(a, b)", "a") == True


def test_3():
    assert operacoes.match(".(a, b)", "ab") == True


def test_4():
    assert operacoes.match("*(+(a, b))", "a") == True


def test_5():
    assert operacoes.match("*(+(a, b))", "aaa") == True


def test_6():
    assert operacoes.match("*(+(a, b))", "ab") == True


def test_7():
    assert operacoes.match("*(+(a, b))", "aba") == True


def test_8():
    assert operacoes.match("*(+(a, b))", "abababa") == True


def test_9():
    assert operacoes.match('.(*(+(a,b)), *(+(+(a,b),c)))', 'ababababbabacababacbacb') == True


def test_10():
    assert operacoes.match(".(.(*(+(a,b)), .(a,.(b,.(b,a)))), *(+(a,b)))", "baabbaba") == True


def test_11():
    assert operacoes.match(".(.(0,*(+(0,1))),1)", "0001010") == False


def test_12():
    assert operacoes.match(".(*(1), *(.(.(0,*(1)), .(0,*(1)))))", "1100") == True


def test_13():
    assert operacoes.match(".(*(+(1, .(0,1))), +(e,0))", "11101010110") == True

def test_14():
    assert operacoes.match('.(*(+(*(.(a,b)),c)), +(*(.(a,b)),c))', 'cccccabab') == True

def test_15():
    assert operacoes.match(".(*(+(z, .(a,z))), +(e,a))", "zzzazazazza") == True