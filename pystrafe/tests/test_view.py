import math
from pytest import warns, approx
from pystrafe import view

def test_angles_to_vectors_2d():
    assert view.angles_to_vectors(0, 0, 2) == ([1, 0], [0, -1])
    assert view.angles_to_vectors(math.radians(45), 0, 2) == ([1, 0], [0, -1])
    assert view.angles_to_vectors(math.radians(30), math.radians(115), 2) \
            == ([approx(-0.42261826174069933), approx(0.90630778703665)],
                [approx(0.90630778703665), approx(0.42261826174069933)])

def test_angles_to_vectors_3d():
    assert view.angles_to_vectors(0, 0, 3) == ([1, 0, 0], [0, -1, 0])
    rad25 = math.radians(25)
    rad115 = math.radians(115)
    radneg80 = math.radians(-80)
    assert view.angles_to_vectors(math.radians(-80), math.radians(115), 3) \
        == ([approx(math.cos(rad115) * math.cos(radneg80)),
             approx(math.sin(rad115) * math.cos(radneg80)),
             approx(math.sin(-radneg80))],
            [approx(math.cos(rad25)), approx(math.sin(rad25)), 0])
    assert view.angles_to_vectors(math.pi / 2, 0, 3) \
        == ([approx(0), approx(0), approx(-1)], [approx(0), approx(-1), approx(0)])

def test_angles_to_vectors_gimbal_lock():
    with warns(RuntimeWarning):
        assert view.angles_to_vectors(math.radians(90), 0, 2) \
                == ([1, 0], [0, -1])
    with warns(RuntimeWarning):
        assert view.angles_to_vectors(math.radians(-270), 348, 2) \
                == ([approx(-0.7539220584369601), approx(0.6569638725243396)],
                    [approx(0.6569638725243396), approx(0.7539220584369601)])
