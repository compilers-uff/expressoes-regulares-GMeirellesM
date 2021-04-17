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