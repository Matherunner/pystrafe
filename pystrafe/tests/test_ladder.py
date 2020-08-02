import math
from pystrafe import ladder, view
from pytest import approx, raises

pi_2 = 0.5 * math.pi
pi_4 = 0.25 * math.pi

def test_climb_velocity():
    fv, sv = view.angles_to_vectors(-pi_2, pi_2, 3)
    assert ladder.climb_velocity([1, 0, 0], fv, sv, 1, -1) == [approx(0), approx(0), approx(400)]
    fv, sv = view.angles_to_vectors(-pi_2, math.radians(135), 3)
    assert ladder.climb_velocity([math.cos(-pi_4), math.sin(-pi_4), 0], fv, sv, 1, 0) \
        == [approx(0), approx(0), approx(200)]

def test_climb_velocity_2d():
    with raises(IndexError):
        ladder.climb_velocity([1, 0], [-1, 0], [0, 1], 1, 1)

def test_maxspeed_normal_2d():
    with raises(IndexError):
        ladder.maxspeed_normal([1, 0], 1, 1, 1)

def test_maxspeed_normal_combinations():
    assert ladder.maxspeed_normal([1, 0, 0], 1, 1, 1) == (-pi_2, -pi_2)
    assert ladder.maxspeed_normal([1, 0, 0], 1, 1, -1) == (-pi_2, pi_2)
    assert ladder.maxspeed_normal([1, 0, 0], 1, -1, 1) == (pi_2, -pi_2)
    assert ladder.maxspeed_normal([1, 0, 0], 1, -1, -1) == (pi_2, pi_2)
    assert ladder.maxspeed_normal([1, 0, 0], -1, 1, 1) == (pi_2, pi_2)
    assert ladder.maxspeed_normal([1, 0, 0], -1, 1, -1) == (pi_2, -pi_2)
    assert ladder.maxspeed_normal([1, 0, 0], -1, -1, 1) == (-pi_2, pi_2)
    assert ladder.maxspeed_normal([1, 0, 0], -1, -1, -1) == (-pi_2, -pi_2)

def test_maxspeed_normal_not1_signs():
    assert ladder.maxspeed_normal([1, 0, 0], 1e10, 1e-10, 1e10) == (-pi_2, -pi_2)
    assert ladder.maxspeed_normal([1, 0, 0], -1e30, -1e30, 1e-20) == (-pi_2, pi_2)

def test_maxspeed_normal_pos_nz():
    angle = math.radians(30)
    n = [0, math.cos(angle), math.sin(angle)]
    assert ladder.maxspeed_normal(n, 1, 1, 1) == (approx(-0.3747344327087402), approx(-0.7494688654174801))
    angle = math.radians(80)
    n = [math.cos(angle), 0, math.sin(angle)]
    assert ladder.maxspeed_normal(n, 1, 1, 1) == (approx(0.946132171085528), approx(-2.099982918575732))

def test_maxspeed_normal_neg_nz():
    angle = math.radians(-30)
    n = [math.cos(angle), 0, math.sin(angle)]
    assert ladder.maxspeed_normal(n, 1, 1, 1) == (-pi_2, pi_2)
    angle = math.radians(-80)
    n = [0, math.cos(angle), math.sin(angle)]
    assert ladder.maxspeed_normal(n, 1, 1, 1) == (-pi_2, 0)

def test_maxspeed_normal_1_nz():
    assert ladder.maxspeed_normal([0, 0, 1], 1, -1, 1) == (0, None)
    assert ladder.maxspeed_normal([0, 0, -1], -1, 1, -1) == (0, None)

def test_maxspeed_normal_n_length():
    with raises(ValueError):
        ladder.maxspeed_normal([1, 1, 0], 1, 1, 1)
    with raises(ValueError):
        ladder.maxspeed_normal([-1, 1e-3, 0], 1, 1, 1)
    with raises(ValueError):
        tmp = math.sqrt(1 / 3)
        ladder.maxspeed_normal([tmp, tmp, tmp + 1e-3], 1, 1, 1)
