import pytest
from data.input_code.t12 import sort_matrix

class TestSortMatrix:
    # Test with a valid matrix

    # Test with matrix size 1
    def test_sort_matrix_matrix_size_1(self):
        matrix_1 = [[3]]
        expected_result = [[3]]
        assert sort_matrix(matrix_1) == expected_result

    # Test with empty matrix
    def test_sort_matrix_empty_matrix(self):
        matrix_1 = []
        assert sort_matrix(matrix_1) == []

    # Test with matrix containing empty rows

    # Test with matrix containing None values

    # Test with very large matrix
    def test_sort_matrixlarge_matrix(self):
        import random
        matrix_1 = [random.sample(range(1000), 3) for _ in range(50)]
        sorted_matrix_1 = sorted(matrix_1, key=sum)
        assert sort_matrix(matrix_1) == sorted_matrix_1