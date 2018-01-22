from pystrafe import common

def test_vec_cross():
    assert common.vec_cross([4, 1, 2], [4, 1, 2]) == [0, 0, 0]
    assert common.vec_cross([-3, 2, 3], [3, -2, 5]) == [16, 24, 0]
