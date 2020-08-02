import math
from pytest import approx
from pystrafe import common

def test_float_equal():
    assert common.float_equal(1.5, 1.5 + 1e-10)
    assert not common.float_equal(1.5, 1.5 - 1e-4)

def test_float_zero():
    assert common.float_zero(1e-10)
    assert not common.float_zero(1e-4)

def test_vec_cross():
    assert common.vec_cross([4, 1, 2], [4, 1, 2]) == [0, 0, 0]
    assert common.vec_cross([-3, 2, 3], [3, -2, 5]) == [16, 24, 0]

def test_vec_add():
    v = [1, 2, 3]
    common.vec_add(v, [4, 8, 1])
    assert v == [5, 10, 4]

def test_vec_sub():
    v = [1, 2, 3]
    common.vec_sub(v, [-4, -8, -1])
    assert v == [5, 10, 4]

def test_vec_mul():
    v = [1, 2, -1]
    common.vec_mul(v, 4)
    assert v == [4, 8, -4]
    v = [10, 100, -100]
    common.vec_mul(v, 0)
    assert v == [0, 0, 0]

def test_vec_normalize():
    v = [3, 0, 4]
    common.vec_normalize(v)
    assert v == [approx(3 / 5), 0, approx(4 / 5)]
    v = [0, -100]
    common.vec_normalize(v)
    assert v == [0, -1]

def test_vec_dot():
    assert common.vec_dot([3, 1, -8], [2, -1.5, 2], 3) == approx(-11.5)
    assert common.vec_dot([1, 1], [-1, 1], 2) == 0.0
    assert common.vec_dot([0, 0], [0, 0, 0, 0], 2) == 0.0

def test_vec_length():
    assert common.vec_length([3, 1, -2], 3) == approx(3.741657387)

def test_anglemod_rad():
    assert common.anglemod_rad(0) == 0
    assert common.anglemod_rad(math.radians(10)) == 1820 * common.anglemod_u_rad
    assert common.anglemod_rad(math.radians(-350)) == 1821 * common.anglemod_u_rad
    assert common.anglemod_rad(math.pi / 4) == math.pi / 4

def test_anglemod_deg():
    assert common.anglemod_deg(0) == 0
    assert common.anglemod_deg(30) == 5461 * common.anglemod_u_deg
    assert common.anglemod_deg(-330) == 5462 * common.anglemod_u_deg
