import pytest
from data.input_code.t6 import *

@pytest.mark.parametrize('x, expected', [
    (8, True),
    (10, False)
])
def test_is_Power_Of_Two_success(x, expected):
    assert is_Power_Of_Two(x) == expected

def test_is_Power_Of_Two_error():
    with pytest.raises(ValueError):
        is_Power_Of_Two(0)

@pytest.mark.parametrize('a, b, expected', [
    (8, 7, True),
    (8, 8, False),
    (8, 9, True)
])
def test_differ_At_One_Bit_Pos(a, b, expected):
    assert differ_At_One_Bit_Pos(a, b) == expected

def test_differ_At_One_Bit_Pos_error():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error2():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error3():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error4():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error5():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error6():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error7():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error8():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error9():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error10():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error11():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error12():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error13():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error14():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error15():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error16():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error17():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error18():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error19():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error20():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error21():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error22():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error23():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error24():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error25():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error26():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error27():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error28():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error29():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error30():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error31():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error32():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error33():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error34():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error35():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error36():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error37():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error38():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error39():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error40():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error41():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error42():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error43():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error44():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error45():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error46():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error47():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error48():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error49():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error50():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error51():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error52():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error53():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error54():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error55():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error56():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error57():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error58():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error59():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error60():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error61():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error62():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error63():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error64():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error65():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error66():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error67():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error68():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error69():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error70():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error71():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error72():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error73():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error74():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error75():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error76():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error77():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error78():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error79():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error80():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error81():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error82():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error83():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error84():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error85():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error86():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error87():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error88():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error89():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error90():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error91():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error92():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error93():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error94():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error95():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error96():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error97():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error98():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error99():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error100():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error101():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error102():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error103():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error104():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error105():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error106():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error107():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error108():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error109():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error110():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error111():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error112():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error113():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error114():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error115():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error116():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error117():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error118():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error119():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error120():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error121():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error122():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error123():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error124():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error125():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error126():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error127():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error128():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error129():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error130():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error131():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error132():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error133():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error134():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error135():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error136():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error137():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error138():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error139():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error140():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error141():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error142():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error143():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error144():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error145():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error146():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error147():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error148():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error149():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error150():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error151():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error152():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error153():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error154():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error155():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error156():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error157():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error158():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error159():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error160():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error161():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error162():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error163():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error164():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error165():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error166():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error167():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error168():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error169():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error170():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error171():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error172():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error173():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error174():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error175():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error176():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error177():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error178():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error179():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error180():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error181():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error182():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error183():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error184():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error185():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error186():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error187():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error188():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error189():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error190():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error191():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error192():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error193():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error194():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error195():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error196():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error197():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error198():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error199():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error200():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error201():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error202():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error203():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error204():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error205():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error206():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error207():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error208():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error209():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error210():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error211():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error212():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error213():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error214():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error215():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error216():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error217():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error218():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error219():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error220():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error221():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error222():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error223():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error224():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error225():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error226():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error227():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error228():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error229():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error230():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error231():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error232():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error233():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error234():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error235():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error236():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error237():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error238():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error239():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error240():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error241():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error242():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error243():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error244():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error245():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error246():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error247():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error248():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error249():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error250():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error251():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error252():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error253():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error254():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error255():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error256():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error257():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error258():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error259():
    with pytest.raises(ValueError):
        differ_At_One_Bit_Pos(8, 8)

def test_differ_At_One_Bit_Pos_error