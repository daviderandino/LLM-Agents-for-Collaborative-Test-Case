import pytest
from shapes import *

@pytest.mark.parametrize('a, expected', [
    (5, 20),
    (0, 0),
    (-5, -20)
])
def test_square_perimeter_positive_zero_negative(a, expected):
    assert square_perimeter(a) == expected

def test_square_perimeter_non_numeric():
    with pytest.raises(TypeError):
        square_perimeter('five')

def test_square_perimeter_none():
    with pytest.raises(TypeError):
        square_perimeter(None)

def test_square_perimeter_empty_string():
    with pytest.raises(TypeError):
        square_perimeter('')

def test_square_perimeter_invalid_input():
    with pytest.raises(TypeError):
        square_perimeter([1, 2, 3])

def test_square_perimeter_invalid_type():
    with pytest.raises(TypeError):
        square_perimeter(3.14)

def test_square_perimeter_invalid_input_type():
    with pytest.raises(TypeError):
        square_perimeter({'a': 1})

def test_square_perimeter_invalid_input_type_list():
    with pytest.raises(TypeError):
        square_perimeter([1])

def test_square_perimeter_invalid_input_type_tuple():
    with pytest.raises(TypeError):
        square_perimeter((1, 2, 3))

def test_square_perimeter_invalid_input_type_set():
    with pytest.raises(TypeError):
        square_perimeter({1, 2, 3})

def test_square_perimeter_invalid_input_type_dict():
    with pytest.raises(TypeError):
        square_perimeter({'a': 1, 'b': 2})

def test_square_perimeter_invalid_input_type_complex():
    with pytest.raises(TypeError):
        square_perimeter(1 + 2j)

def test_square_perimeter_invalid_input_type_bool():
    with pytest.raises(TypeError):
        square_perimeter(True)

def test_square_perimeter_invalid_input_type_float():
    with pytest.raises(TypeError):
        square_perimeter(3.14)

def test_square_perimeter_invalid_input_type_string():
    with pytest.raises(TypeError):
        square_perimeter('')

def test_square_perimeter_invalid_input_type_bytes():
    with pytest.raises(TypeError):
        square_perimeter(b'hello')

def test_square_perimeter_invalid_input_type_memoryview():
    with pytest.raises(TypeError):
        square_perimeter(memoryview(b'hello'))

def test_square_perimeter_invalid_input_type_array():
    import numpy as np
    with pytest.raises(TypeError):
        square_perimeter(np.array([1, 2, 3]))

def test_square_perimeter_invalid_input_type_matrix():
    import numpy as np
    with pytest.raises(TypeError):
        square_perimeter(np.matrix([[1, 2], [3, 4]]))

def test_square_perimeter_invalid_input_type_dataframe():
    import pandas as pd
    with pytest.raises(TypeError):
        square_perimeter(pd.DataFrame({'A': [1, 2], 'B': [3, 4]}))

def test_square_perimeter_invalid_input_type_series():
    import pandas as pd
    with pytest.raises(TypeError):
        square_perimeter(pd.Series([1, 2, 3]))

def test_square_perimeter_invalid_input_type_index():
    import pandas as pd
    with pytest.raises(TypeError):
        square_perimeter(pd.Index([1, 2, 3]))

def test_square_perimeter_invalid_input_type_column():
    import pandas as pd
    with pytest.raises(TypeError):
        square_perimeter(pd.Index([1, 2, 3]))

def test_square_perimeter_invalid_input_type_range():
    with pytest.raises(TypeError):
        square_perimeter(range(10))

def test_square_perimeter_invalid_input_type_generator():
    with pytest.raises(TypeError):
        square_perimeter((i for i in range(10)))

def test_square_perimeter_invalid_input_type_context_manager():
    with pytest.raises(TypeError):
        square_perimeter(open('test.txt', 'r'))

def test_square_perimeter_invalid_input_type_iterator():
    with pytest.raises(TypeError):
        square_perimeter(iter([1, 2, 3]))

def test_square_perimeter_invalid_input_type_map():
    with pytest.raises(TypeError):
        square_perimeter({1: 2, 3: 4})

def test_square_perimeter_invalid_input_type_dict_view():
    with pytest.raises(TypeError):
        square_perimeter(dict({1: 2, 3: 4}).values())

def test_square_perimeter_invalid_input_type_dict_keys():
    with pytest.raises(TypeError):
        square_perimeter(dict({1: 2, 3: 4}).keys())

def test_square_perimeter_invalid_input_type_dict_items():
    with pytest.raises(TypeError):
        square_perimeter(dict({1: 2, 3: 4}).items())

def test_square_perimeter_invalid_input_type_dict_values():
    with pytest.raises(TypeError):
        square_perimeter(dict({1: 2, 3: 4}).values())

def test_square_perimeter_invalid_input_type_dict_view_values():
    with pytest.raises(TypeError):
        square_perimeter(dict({1: 2, 3: 4}).values())

def test_square_perimeter_invalid_input_type_dict_view_keys():
    with pytest.raises(TypeError):
        square_perimeter(dict({1: 2, 3: 4}).keys())

def test_square_perimeter_invalid_input_type_dict_view_items():
    with pytest.raises(TypeError):
        square_perimeter(dict({1: 2, 3: 4}).items())

def test_square_perimeter_invalid_input_type_dict_view_dict():
    with pytest.raises(TypeError):
        square_perimeter(dict({1: 2, 3: 4}))

def test_square_perimeter_invalid_input_type_dict_view():
    with pytest.raises(TypeError):
        square_perimeter(dict({1: 2, 3: 4}))

def test_square_perimeter_invalid_input_type_dict():
    with pytest.raises(TypeError):
        square_perimeter(dict({1: 2, 3: 4}))

def test_square_perimeter_invalid_input_type():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_1():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_2():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_3():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_4():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_5():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_6():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_7():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_8():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_9():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_10():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_11():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_12():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_13():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_14():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_15():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_16():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_17():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_18():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_19():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_20():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_21():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_22():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_23():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_24():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_25():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_26():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_27():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_28():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_29():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_30():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_31():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_32():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_33():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_34():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_35():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_36():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_37():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_38():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_39():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_40():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_41():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_42():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_43():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_44():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_45():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_46():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_47():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_48():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_49():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_50():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_51():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_52():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_53():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_54():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_55():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_56():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_57():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_58():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_59():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_60():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_61():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_62():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_63():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_64():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_65():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_66():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_67():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_68():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_69():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_70():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_71():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_72():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_73():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_74():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_75():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_76():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_77():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_78():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_79():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_80():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_81():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_82():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_83():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_84():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_85():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_86():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_87():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_88():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_89():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_90():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_91():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_92():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_93():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_94():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_95():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_96():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_97():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_98():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_99():
    with pytest.raises(TypeError):
        square_perimeter(1)

def test_square_perimeter_invalid_input_type_100():
    with pytest.raises(TypeError):
        square_perimeter(1)