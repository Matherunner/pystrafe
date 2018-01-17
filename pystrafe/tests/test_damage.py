import math
import itertools
import numpy as np
from pytest import approx, raises
from pystrafe import damage

def test_hpap_damage():
    assert damage.hpap_damage(100, 100, 100) == (80, 60)
    assert damage.hpap_damage(100, 100, 300) == (0, 0)
    assert damage.hpap_damage(100, 0, 0.99999) == (100, 0)
    assert damage.hpap_damage(100, 0, 1) == (99, 0)

def test_hpap_damage_zero_ap():
    hps = range(-1000, 1001, 10)
    dmgs = range(-1000, 1001, 10)
    for hp, dmg in itertools.product(hps, dmgs):
        assert damage.hpap_damage(hp, 0, dmg) == (hp - dmg, 0)

def test_hpap_damage_zero_hp():
    aps = range(-1000, 1001, 10)
    dmgs = range(0, 1001, 10)
    for ap, dmg in itertools.product(aps, dmgs):
        assert damage.hpap_damage(0, ap, dmg)[0] <= 0

def test_hpap_damage_neg_dmg():
    assert damage.hpap_damage(100, 0, -1) == (101, 0)
    assert damage.hpap_damage(100, 0, -1234) == (1334, 0)
    assert damage.hpap_damage(100, 0, -1.5) == (101, 0)
    assert damage.hpap_damage(100, 1, -1) == (100, 1.4)
    assert damage.hpap_damage(100, 100, -1) == (100, 100.4)
    assert damage.hpap_damage(100, 1, -4) == (100, 2.6)
    assert damage.hpap_damage(100, 1, -5) == (101, 3)
    assert damage.hpap_damage(100, 0.001, -100) == (120, 40.001)

def test_hpap_damage_neg_ap():
    assert damage.hpap_damage(100, -1, 70) == (28, 0)
    assert damage.hpap_damage(100, -5, 70) == (20, 0)
    assert damage.hpap_damage(100, -1, 0) == (98, 0)

def test_fall():
    assert damage.fall(-100) == 0.0
    assert damage.fall(0) == 0.0
    assert damage.fall(580) == 0.0
    assert damage.fall(581) == 25 / 111
    assert damage.fall(1000) == approx(94.5945945945946)
    assert damage.fall(1024) == approx(100)

def test_ap_dhp_damage_pos_dhp_pos_dmg():
    assert damage.ap_dhp_damage(20, 40) == (9.5, 10, '(', ']')
    assert damage.ap_dhp_damage(20, 70) == (24.5, 25.0, '(', ']')
    assert damage.ap_dhp_damage(20, 103) == (41, 41.2, '(', 'inf')

def test_ap_dhp_damage_zero_dhp():
    assert damage.ap_dhp_damage(0, 0) == (-0.5, 0, '(', 'inf')
    assert damage.ap_dhp_damage(0, 1) == (0, 0.4, '(', 'inf')
    assert damage.ap_dhp_damage(0, 2) == (0.5, 0.8, '(', 'inf')
    assert damage.ap_dhp_damage(0, -1) == (-1, -0.5, '(', ']')
    for dmg in np.arange(0, 5, 0.05):
        apl, apu, t1, t2 = damage.ap_dhp_damage(0, dmg)
        assert (t1, t2) == ('(', 'inf')
        assert damage.hpap_damage(100, apl, dmg) == (99, 0)
        assert damage.hpap_damage(100, apl + 1e-4, dmg) == (100, 0)
        assert damage.hpap_damage(100, apu, dmg) == (100, 0)

    assert damage.ap_dhp_damage(0, 5) == (math.nan, math.nan, None, None)
    for dmg in range(5, 100, 2):
        assert damage.ap_dhp_damage(0, dmg)[2] is None

def test_ap_dhp_damage_equal_dhp_dmg():
    assert damage.ap_dhp_damage(-1.999, -1) == (0, 0, '[', ']')
    assert damage.ap_dhp_damage(-101, -101) == (0, 0, '[', ']')
    assert damage.ap_dhp_damage(1.3, 1) == (-0.5, 0, '(', ']')

def test_ap_dhp_damage_neg_dhp_pos_dmg():
    assert damage.ap_dhp_damage(-10, 6) == (math.nan, math.nan, None, None)
    assert damage.ap_dhp_damage(-1, 1e-4) == (math.nan, math.nan, None, None)
    assert damage.ap_dhp_damage(-1, 0) == (math.nan, math.nan, None, None)
    assert damage.ap_dhp_damage(-0.9999, 0) == (-0.5, 0, '(', 'inf')
    assert damage.ap_dhp_damage(-0.0001, 2) == (0.5, 0.8, '(', 'inf')

def test_ap_dhp_damage_pos_dhp_neg_dmg():
    assert damage.ap_dhp_damage(10, -1) == (-6, -5.5, '(', ']')
    assert damage.ap_dhp_damage(10, -10) == (-10.5, -10, '(', ']')
    assert damage.ap_dhp_damage(10, -100) == (-55.5, -55, '(', ']')

def test_ap_dhp_damage_big_dmg():
    assert damage.ap_dhp_damage(1, 9.9) == (approx(3.95), approx(3.96), '(', 'inf')
    assert damage.ap_dhp_damage(1, 9.9999) == (approx(3.99995), approx(3.99996), '(', 'inf')
    assert damage.ap_dhp_damage(1, 10) == (math.nan, math.nan, None, None)
    assert damage.ap_dhp_damage(1, 11) == (math.nan, math.nan, None, None)
    for dhp, mult in itertools.product(range(0, 1001, 10), range(5, 20)):
        dmg = dhp * mult + 5
        assert damage.ap_dhp_damage(dhp, dmg) == (math.nan, math.nan, None, None)

def test_ap_dhp_damage_dhp_gt_dmg():
    assert damage.ap_dhp_damage(21, 20) == (-1, -0.5, '(', ']')
    assert damage.ap_dhp_damage(20.9999, 20) == (-0.5, 0, '(', ']')
    assert damage.ap_dhp_damage(20, 20) == (-0.5, 0, '(', ']')
    assert damage.ap_dhp_damage(0.9, 0) == (-0.5, 0, '(', 'inf')
    assert damage.ap_dhp_damage(100, 0) == (-50.5, -50, '(', ']')
    for dhp, dmg in [(20, 10), (50, 10), (1000, 10), (50, 0), (100, 0)]:
        apl, apu, t1, t2 = damage.ap_dhp_damage(dhp, dmg)
        assert (t1, t2) == ('(', ']')
        assert apl < 0
        assert apu < 0

def test_ap_dhp_damage_input_to_hpap_damage():
    dhps = np.arange(-100, 101, 0.47)
    dmgs = np.arange(-100, 101, 0.47)
    for dhp, dmg in itertools.product(dmgs, dhps):
        apl, apu, t1, t2 = damage.ap_dhp_damage(dhp, dmg)
        if t1 == '[':
            hp, ap = damage.hpap_damage(100, apl, dmg)
            assert 100 - hp == int(dhp)
        elif t1 == '(':
            hp, ap = damage.hpap_damage(100, apl + 1e-4, dmg)
            assert 100 - hp == int(dhp)
            hp, ap = damage.hpap_damage(100, apl, dmg)
            assert 100 - hp - 1 == int(dhp)
        if t2 == ']':
            hp, ap = damage.hpap_damage(100, apu, dmg)
            assert 100 - hp == int(dhp)
        elif t2 == ')':
            hp, ap = damage.hpap_damage(100, apu - 1e-4, dmg)
            assert 100 - hp == int(dhp)
            hp, ap = damage.hpap_damage(100, apu, dmg)
            assert 100 - hp + 1 == int(dhp)
        elif t2 == 'inf':
            hp, ap = damage.hpap_damage(100, 1234567, dmg)
            assert ap > 0
            assert 100 - hp == int(dhp)
            hp, ap = damage.hpap_damage(100, apu, dmg)
            assert ap == 0
