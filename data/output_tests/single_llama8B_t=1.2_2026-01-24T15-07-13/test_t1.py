import pytest
from data.input_code.t1 import min_cost, R, C



def test_min_cost_empty_list():
    with pytest.raises(IndexError):
        min_cost([], 3, 3)


def test_min_cost_out_of_bounds():
    cost = [[1 for _ in range(C+1)] for _ in range(R+1)]
    def min_cost_side_effect():
        for i in range(R+1):
            for j in range(C+1):
                print(f"i: {i}, j: {j}")
                cost[i][j] = 0
        return cost[R][C]
    min_cost = min_cost_side_effect
    pytest.raises(Exception, min_cost, cost, R, C)