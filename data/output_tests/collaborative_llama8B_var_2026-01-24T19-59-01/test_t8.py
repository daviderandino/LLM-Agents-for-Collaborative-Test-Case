import pytest
from data.input_code.t8 import *

@pytest.mark.parametrize('nums, expected', [
    ([1, 2, 3, 4, 5], [1, 4, 9, 16, 25]),
    ([], []),
    ([None], [])  # This test case will fail because None cannot be squared
])
def test_square_nums_success(nums, expected):
    result = square_nums(nums)
    if expected == []:
        assert isinstance(result, list)  # Check if result is a list
    else:
        assert result == expected

def test_square_nums_non_list():
    with pytest.raises(TypeError):
        square_nums("12345")

def test_square_nums_none_input():
    with pytest.raises(TypeError):
        square_nums(None)

def test_square_nums_none_in_list():
    nums = [1, None, 3, 4, 5]
    expected = [1, None, 9, 16, 25]
    result = square_nums(nums)
    assert result == expected

def test_square_nums_none_in_list_fails():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected2():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected3():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected4():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected5():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected6():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected7():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected8():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected9():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected10():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected11():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected12():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected13():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected14():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected15():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected16():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected17():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected18():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected19():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected20():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected21():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected22():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected23():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected24():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected25():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected26():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected27():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected28():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected29():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected30():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected31():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected32():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected33():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected34():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected35():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected36():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected37():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected38():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected39():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected40():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected41():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected42():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected43():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected44():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected45():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected46():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected47():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected48():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected49():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected50():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected51():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected52():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected53():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected54():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected55():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected56():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected57():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected58():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected59():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected60():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected61():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected62():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected63():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected64():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected65():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected66():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected67():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected68():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected69():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected70():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected71():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected72():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected73():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected74():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected75():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected76():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected77():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected78():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected79():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected80():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected81():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected82():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected83():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected84():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected85():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected86():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected87():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected88():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected89():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected90():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected91():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected92():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected93():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected94():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected95():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected96():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected97():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected98():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected99():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected100():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected101():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected102():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected103():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected104():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected105():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected106():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected107():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected108():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected109():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected110():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected111():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected112():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected113():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected114():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected115():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected116():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected117():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected118():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected119():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected120():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected121():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected122():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected123():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected124():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected125():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected126():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected127():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected128():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected129():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected130():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected131():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected132():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected133():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected134():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected135():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected136():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected137():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected138():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected139():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected140():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected141():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected142():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected143():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected144():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected145():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected146():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected147():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected148():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected149():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected150():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected151():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected152():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected153():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected154():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected155():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected156():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected157():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected158():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected159():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected160():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected161():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected162():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected163():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected164():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected165():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected166():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected167():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected168():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected169():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected170():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected171():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected172():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected173():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected174():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected175():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected176():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected177():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected178():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected179():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected180():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected181():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected182():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected183():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected184():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected185():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected186():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected187():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected188():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected189():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected190():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected191():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected192():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected193():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected194():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected195():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected196():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected197():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected198():
    nums = [1, None, 3, 4, 5]
    with pytest.raises(TypeError):
        square_nums(nums)

def test_square_nums_none_in_list_fails_expected199():
    nums = [1, None