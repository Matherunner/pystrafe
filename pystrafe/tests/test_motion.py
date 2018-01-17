import math
import itertools
import numpy as np
from pytest import raises, approx
from pystrafe import motion

def test_strafe_K():
    with raises(ZeroDivisionError):
        motion.strafe_K(0, 0, 0, 0)
    assert motion.strafe_K(30, 0.001, 320, 0) == 0.0
    assert motion.strafe_K(30, 0.01, 320, 10) == approx(90000)
    assert motion.strafe_K(30, 0.001, 320, 10) == approx(181760)
    assert motion.strafe_K(320, 0.001, 320, 10) == approx(2037760)
    assert motion.strafe_K(320, 0.001, 320, 2000) == approx(102400000)
    assert motion.strafe_K(30, 0.001, 10, 10) == approx(1990)
    assert motion.strafe_K(30, 0.001, 0, 10) == 0

def test_strafe_K_neg_params():
    with raises(ValueError):
        motion.strafe_K(-10, 10, 10, 10)
    with raises(ValueError):
        motion.strafe_K(10, -10, 10, 10)
    with raises(ValueError):
        motion.strafe_K(10, 10, -10, 10)
    with raises(ValueError):
        motion.strafe_K(10, -10, 10, -10)

def test_strafe_speedxf():
    with raises(ValueError):
        motion.strafe_speedxf(4, 450, -10)
    assert motion.strafe_speedxf(4, 450, 0) == 450
    assert motion.strafe_speedxf(0, 0, 0) == 0
    K = motion.strafe_K(30, 0.001, 320, 10)
    assert motion.strafe_speedxf(4, 450, K) == approx(964.12654771)
    assert motion.strafe_speedxf(0, 987, K) == 987
    K = motion.strafe_K(30, 0.001, 320, 100)
    assert motion.strafe_speedxf(4.2, 0, K) == approx(1944.222209522)
    K = motion.strafe_K(320, 0.01, 320, 10)
    assert motion.strafe_speedxf(2, 100, K) == approx(1975.145564256)

def test_strafe_speedxf_neg_time():
    K = motion.strafe_K(320, 0.01, 320, 10)
    with raises(ValueError):
        motion.strafe_speedxf(-1, 0, K)
    assert motion.strafe_speedxf(-1, 1451.068571777, K) == approx(400)

def test_strafe_distance():
    K = motion.strafe_K(30, 0.001, 320, 10)
    with raises(ValueError):
        motion.strafe_distance(1, 100, -K)
    assert motion.strafe_distance(0, 456, K) == 0
    assert motion.strafe_distance(0, 1e5, 1e8) == 0
    assert motion.strafe_distance(1, 100, K) == approx(304.32984903732694)
    K = motion.strafe_K(30, 0.01, 320, 10)
    assert motion.strafe_distance(2.5, 1, K) == approx(790.5746781033104)
    assert motion.strafe_distance(1, -100, K) == approx(226.83538223469472)
    assert motion.strafe_distance(1, 953.93920141694559, K) == approx(977.15056822651479)

def test_strafe_distance_neg_time():
    K = motion.strafe_K(30, 0.01, 320, 10)
    with raises(ValueError):
        motion.strafe_distance(-1, 100, K)
    assert motion.strafe_distance(-1, 1000, K) == approx(977.15056822651479)

def test_strafe_distance_zero_K():
    assert motion.strafe_distance(1, 100, 1) == approx(100.00249995834504)
    assert motion.strafe_distance(1, 100, 1e-5) == approx(100.00000086923438)
    assert motion.strafe_distance(1, 100, 0) == 100
    assert motion.strafe_distance(1, -100, 0) == 100

def test_strafe_time():
    assert motion.strafe_time(400, 400, 1e-5) == approx(0.9999901521950959)
    assert motion.strafe_time(400, 400, 0) == approx(1)
    assert motion.strafe_time(0, 400, 0) == approx(0)
    assert motion.strafe_time(1, 0, 0) == math.inf
    K = motion.strafe_K(30, 0.001, 320, 10)
    with raises(ValueError):
        motion.strafe_time(100, 320, -K)
    assert motion.strafe_time(100000, 320, K) == approx(49.314635892504114)
    assert motion.strafe_time(100, 320, K) == approx(0.28012970263654435)
    assert motion.strafe_time(0, 320, K) == approx(0)
    assert motion.strafe_time(-100, 320, K) == approx(0.28012970263654435)
    assert motion.strafe_time(-100, -320, K) == approx(0.28012970263654435)
    K = motion.strafe_K(30, 0.001, 320, 100)
    assert motion.strafe_time(1000, 320, K) == approx(1.2653051142112355)
    assert motion.strafe_time(0, 320, K) == approx(0)

def test_strafe_time_extremes():
    K = motion.strafe_K(30, 0.001, 320, 10)
    xs = [0, 1e-15, 1e-10, 1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2]
    vs = [0, 1, 1e1, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9, 1e10, 1e15]
    for x, v in itertools.product(xs, vs):
        assert motion.strafe_time(x, v, K) >= 0

def test_gravity_speediz_distance_time_zero_t():
    assert motion.gravity_speediz_distance_time(0, 1, 800) == math.inf
    assert motion.gravity_speediz_distance_time(0, -1, 800) == -math.inf
    with raises(ValueError):
        motion.gravity_speediz_distance_time(0, 0, 800)
    with raises(ValueError):
        motion.gravity_speediz_distance_time(0, 0, 0)
    assert motion.gravity_speediz_distance_time(0, 1, 0) == math.inf
    assert motion.gravity_speediz_distance_time(0, -1, 0) == -math.inf

def test_gravity_time_speediz_z():
    assert motion.gravity_time_speediz_z(10, 10, 0) == (1, 1)
    with raises(ZeroDivisionError):
        motion.gravity_time_speediz_z(0, 10, 0)
    assert motion.gravity_time_speediz_z(0, 0, 800) == (0, 0)
    with raises(ValueError):
        motion.gravity_time_speediz_z(0, 10, 800)
    ret = motion.gravity_time_speediz_z(0, 10, -800)
    assert ret[0] == approx(0.15811388300841897)
    assert ret[1] == approx(-0.15811388300841897)
    ret = motion.gravity_time_speediz_z(0, -10, 800)
    assert ret[0] == approx(-0.15811388300841897)
    assert ret[1] == approx(0.15811388300841897)
    ret = motion.gravity_time_speediz_z(-100, 6.25, 800)
    assert ret[0] == approx(-0.125)
    assert ret[0] == approx(ret[1])
    ret = motion.gravity_time_speediz_z(268, 20, 800)
    assert ret[0] == approx(0.085550606334671569)
    assert ret[1] == approx(0.58444939366532844)
    ret = motion.gravity_time_speediz_z(268, -20, 560)
    assert ret[0] == approx(-0.069570144084276309)
    assert ret[1] == approx(1.0267130012271333)

def test_gravity_time_speediz_z_curve_shape():
    vs = range(-1000, 1001, 50)
    zs = range(-10000, 10000, 100)
    for v, z in itertools.product(vs, zs):
        try:
            t = motion.gravity_time_speediz_z(v, z, 800)
        except (ZeroDivisionError, ValueError):
            continue
        if math.isclose(t[0], t[1]):
            continue
        assert v - 800 * t[0] > 0
        assert v - 800 * t[1] < 0

def test_strafe_solve_speedxi():
    K = motion.strafe_K(30, 0.001, 320, 10)
    with raises(ValueError):
        motion.strafe_solve_speedxi(10, -K, 400, -200, 800)

def test_strafe_solve_speedxi_neg_z():
    K = motion.strafe_K(30, 0.001, 320, 10)
    assert motion.strafe_solve_speedxi(0, K, 100, -18, 800) == approx(450.6474498822009)
    assert motion.strafe_solve_speedxi(0, K, 100, -100, 800) == approx(0)
    assert motion.strafe_solve_speedxi(163.23541222592047, K, 100, -18, 800) == approx(0)
    assert motion.strafe_solve_speedxi(200, K, 100, -18, 800) == approx(0)
    assert motion.strafe_solve_speedxi(0, K, 100, -1e-3, 800) == approx(63245.55095141193)
    assert motion.strafe_solve_speedxi(-10000, K, 100, -100, 800) == approx(10003.952996977921)
    assert motion.strafe_solve_speedxi(-100, K, 200, -200, 800) == approx(248.98914739139963)

def test_strafe_solve_speedxi_pos_z():
    K = motion.strafe_K(30, 0.001, 320, 10)
    assert motion.strafe_solve_speedxi(1000, K, 100, 400, 800) == approx(0)
    with raises(ValueError):
        motion.strafe_solve_speedxi(1000, K, 100, 700, 800)
    with raises(ValueError):
        motion.strafe_solve_speedxi(0, K, 100, 700, 800)

def test_strafe_solve_speedxi_zero_z():
    K = motion.strafe_K(30, 0.001, 320, 10)
    assert motion.strafe_solve_speedxi(1000, K, 1, 0, 800) == math.inf
    assert motion.strafe_solve_speedxi(0, K, 0, 0, 800) == approx(0)
    assert motion.strafe_solve_speedxi(0, K, 100, 0, 800) == math.inf
    assert motion.strafe_solve_speedxi(0, K, 1e-5, 0, 800) == math.inf

def test_strafe_solve_speedxi_zero_x():
    K = motion.strafe_K(30, 0.001, 320, 10)
    with raises(ValueError):
        motion.strafe_solve_speedxi(0, K, 0, 1, 800)
    with raises(ValueError):
        motion.strafe_solve_speedxi(40, K, 0, 2, 800)
    assert motion.strafe_solve_speedxi(40, K, 0, 1, 800) == approx(0)

def test_strafe_solve_speedxi_impossible():
    K = motion.strafe_K(30, 0.001, 320, 10)
    assert math.isnan(motion.strafe_solve_speedxi(-100, K, 0, 2, 800))
    assert math.isnan(motion.strafe_solve_speedxi(-100, K, 10, 2, 800))
    with raises(ValueError):
        motion.strafe_solve_speedxi(0, K, 10, 2, 800)

def test_strafe_solve_speedxi_curve_shape():
    K = motion.strafe_K(30, 0.001, 320, 10)
    xs = range(1, 10000, 500)
    zs = range(1, 601, 100)
    for x, z in itertools.product(xs, zs):
        vix = motion.strafe_solve_speedxi(1000, K, x, z, 800)
        tx = motion.strafe_time(x, vix, K)
        tz = motion.gravity_time_speediz_z(1000, z, 800)
        if not math.isclose(tx, tz[0], abs_tol=1e-6):
            assert tx <= tz[0]

def test_solve_boost_min_dmg():
    K = motion.strafe_K(30, 0.001, 320, 10)
    with raises(ValueError):
        motion.solve_boost_min_dmg([0, 0], -K, 400, 400, 800)

    dv = motion.solve_boost_min_dmg([0, 0], K, 400, 400, 800)
    assert dv[0] == approx(79.399032802535118, 1e-4)
    assert dv[1] == approx(816.5301806366407, 1e-4)
    t = motion.gravity_time_speediz_z(dv[1], 400, 800)
    assert t[1] == approx(motion.strafe_time(400, dv[0], K))
    assert dv[1] - 800 * t[1] <= 0

def test_solve_boost_min_dmg_neg_z():
    K = motion.strafe_K(30, 0.001, 320, 10)
    dv = motion.solve_boost_min_dmg([400, 268], K, 1500, -200, 800)
    assert dv[0] == approx(298.46589871993854, 1e-4)
    assert dv[1] == approx(366.81197893286605, 1e-4)
    K = motion.strafe_K(30, 0.001, 320, 100)
    dv = motion.solve_boost_min_dmg([400, 268], K, 1500, -200, 800)
    assert dv[0] == approx(77.238561539572189, 1e-4)
    assert dv[1] == approx(241.47957829048562, 1e-4)
    dv = motion.solve_boost_min_dmg([0, 0], K, 0, -200, 800)
    assert dv[0] == approx(0)
    assert dv[1] == approx(0)

def test_solve_boost_min_dmg_neg_viz():
    K = motion.strafe_K(30, 0.001, 320, 100)
    dv = motion.solve_boost_min_dmg([0, -600], K, 300, -200, 800)
    assert dv[0] == approx(51.986602324707007)
    assert dv[1] == approx(511.7601499627252)
    tx = motion.strafe_time(300, dv[0], K)
    tz = motion.gravity_time_speediz_z(-600 + dv[1], -200, 800)
    assert tx == approx(tz[1])

    K = motion.strafe_K(30, 0.001, 320, 10)
    dv = motion.solve_boost_min_dmg([0, -600], K, 1000, 500, 800)
    assert dv[0] == approx(520.92144757654194)
    assert dv[1] == approx(1545.1246586237653)
    tx = motion.strafe_time(1000, dv[0], K)
    tz = motion.gravity_time_speediz_z(-600 + dv[1], 500, 800)
    assert tx == approx(tz[1])

def test_solve_boost_min_dmg_range():
    K = motion.strafe_K(30, 0.001, 320, 10)
    for d in itertools.chain(range(-10000, 10001, 100), np.arange(-100, 100, 0.5)):
        dv = motion.solve_boost_min_dmg([0, 0], K, d, d, 800)
        assert dv[0] < 1e4 and dv[1] < 1e4
        assert dv[0] >= 0 and dv[1] >= 0
        t = motion.gravity_time_speediz_z(dv[1], d, 800)
        assert dv[1] - 800 * t[1] <= 0
        strafe_t = motion.strafe_time(d, dv[0], K)
        if not math.isclose(t[1], strafe_t):
            assert t[1] > strafe_t
        if not math.isclose(t[0], strafe_t):
            assert t[0] < strafe_t

        dv = motion.solve_boost_min_dmg(dv, K, d, d, 800)
        assert dv[0] == approx(0, abs=1e-5)
        assert dv[1] == approx(0, abs=1e-5)

        dv = motion.solve_boost_min_dmg([0, 0], K, 400, d, 800)
        assert dv[0] < 1e4 and dv[1] < 1e4

def test_solve_boost_min_dmg_inc_v():
    K = motion.strafe_K(30, 0.001, 320, 10)
    prev = math.inf
    for vx in range(0, 10000, 100):
        dv = motion.solve_boost_min_dmg([vx, 0], K, 1500, -200, 800)
        mag = math.hypot(dv[0], dv[1])
        assert mag <= prev
        prev = mag

    prev = math.inf
    for vy in range(0, 10000, 100):
        dv = motion.solve_boost_min_dmg([0, vy], K, 1500, -200, 800)
        mag = math.hypot(dv[0], dv[1])
        assert mag <= prev
        prev = mag

def test_solve_boost_min_dmg_zero_pos():
    np.warnings.filterwarnings('ignore')
    K = motion.strafe_K(30, 0.001, 320, 10)
    dv = motion.solve_boost_min_dmg([400, 0], K, 0, -1, 800)
    assert dv[0] == approx(0, abs=1e-5)
    assert dv[1] == approx(0, abs=1e-5)
    dv = motion.solve_boost_min_dmg([0, 0], K, 0, 1, 800)
    assert dv[1] >= 1e4
    dv = motion.solve_boost_min_dmg([200, 200], K, 0, 0, 800)
    assert dv[0] == approx(0, abs=1e-5)
    assert dv[1] == approx(0, abs=1e-5)
    np.warnings.filterwarnings('default')

def test_solve_boost_min_dmg_neg_x():
    K = motion.strafe_K(30, 0.001, 320, 10)
    dv1 = motion.solve_boost_min_dmg([0, 0], K, -400, 500, 800)
    dv2 = motion.solve_boost_min_dmg([0, 0], K, 400, 500, 800)
    assert dv1 == dv2

def test_solve_boost_min_dmg_no_dv():
    K = motion.strafe_K(30, 0.001, 320, 10)
    dv = motion.solve_boost_min_dmg([0, 0], K, 100, -100000, 800)
    assert dv[0] == approx(0, abs=1e-5)
    dv = motion.solve_boost_min_dmg([10000, 0], K, 1000, -10, 800)
    assert dv[0] == approx(0, abs=1e-5)
    assert dv[1] == approx(0, abs=1e-5)
    dv = motion.solve_boost_min_dmg([0, 1500], K, 500, 1000, 800)
    assert dv[0] == approx(0, abs=1e-5)
    assert dv[1] == approx(0, abs=1e-5)
