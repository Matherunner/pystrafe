from pytest import approx, warns, raises
from pystrafe import basic

def test_collide():
    v = [-1000, 123, 456]
    basic.collide(v, [1, 0, 0])
    assert v == [0, 123, 456]

def test_collide_out_of_plane():
    v = [100, 100, 100]
    with warns(RuntimeWarning):
        basic.collide(v, [1, 0, 0])
        assert v == [100, 100, 100]
        
def test_collide_2d():
    v = [-200, 200]
    with raises(IndexError):
        basic.collide(v, [1, 0, 0])

def test_collide_b_non_1():
    v = [-100, 0, 0]
    basic.collide(v, [1, 0, 0], 1.5)
    assert v == [50, 0, 0]

def test_collide_b_lt_1():
    v = [-100, 0, 0]
    basic.collide(v, [1, 0, 0], 0.99999)
    assert v == [0, 0, 0]

def test_friction():
    v = [0, 100]
    basic.friction(v, 0.01, basic.E, basic.k)
    assert v == [0, 96]

    v = [2000, 0]
    basic.friction(v, 0.001, basic.E, basic.k)
    assert v == [1992, 0]

def test_friction_zero_speed():
    v = [0, 0]
    basic.friction(v, 0.01, basic.E, basic.k)
    assert v == [0, 0]

def test_frction_3d():
    v = [40, 30, 1234567]
    basic.friction(v, 0.01, basic.E, basic.k)
    assert v == [36.8, 27.6, 1234567]

def test_frction_low_speed():
    v = [1, 1]
    basic.friction(v, 0.01, basic.E, basic.k)
    assert v == [0, 0]

    v = [0, 0.09]
    basic.friction(v, 1e-10, basic.E, basic.k)
    assert v == [0, 0.09]
    basic.friction(v, 10000000, basic.E, basic.k)
    assert v == [0, 0.09]
