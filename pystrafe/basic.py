import math
import warnings
from pystrafe import common

E = 100.0
k = 4.0
g = 800.0

def collide(v, n, b=1):
    """Apply collision to velocity *v* with plane normal *n*.

    Both *v* and *n* vectors must be 3D vectors. The velocity is modified
    in-place and there is no return value. Note that *v* must be directed into
    the plane such that its dot product with *n* is less than or equal to zero.
    If this is not a case, a valid velocity would still be computed, but a
    warning will be raised.
    """
    if not common.float_equal(common.vec_length(n, 3), 1):
        raise ValueError('n must be a unit vector')

    # This is what happens in the game: b is usually never below 1, and the game
    # sets the velocity to zero if that happens.
    if b < 1:
        common.vec_set(v, 0.0, 3)
        return

    vdotn = common.vec_dot(v, n, 3)
    if vdotn > 0.0:
        warnings.warn('v directed out of the plane', RuntimeWarning)
        return

    n = n[:]
    common.vec_mul(n, vdotn * b)
    common.vec_sub(v, n)

def friction(v, tau, E, k):
    """Apply friction to the velocity *v*.

    Only the *x* and *y* components of *v* will be affected. The caller is
    responsible of making sure the player is on the ground when calling this
    function.

    >>> v = [100.0, 0.0]
    >>> friction(v, 0.01, E, k)
    >>> v
    [96.0, 0.0]

    This function does not handle edgefriction and entity friction. The caller
    is responsible of multiplying the coefficients of edgefriction or entity
    friction with *k* as the argument.
    """
    speed = common.vec_length(v, 2)
    if speed < 0.1:
        return
    if speed >= E:
        fric = 1 - tau * k
        common.vec_mul(v, fric, 2)
        return
    fric = tau * E * k
    if speed >= fric:
        vhat = v[:]
        common.vec_mul(vhat, 1 / speed, 2)
        common.vec_mul(vhat, fric, 2)
        common.vec_sub(v, vhat, 2)
    else:
        common.vec_set(v, 0.0, 2)

def gravity_half(v, g, tau):
    """Apply gravity to 3D velocity vector *v*.

    This function will only modify the vertical component of v, that is v[2].

    >>> v = [320.0, 0.0, 100.0]
    >>> gravity_half(v, 800, 0.01)
    >>> v
    [320.0, 0.0, 96.0]
    """
    v[2] -= 0.5 * g * tau

def strafe_fme_theta(v, theta, L, gamma1):
    r"""Perform a general strafe parameterised with theta.

    The convention is such that positive *theta* means strafing towards the
    left, and vice versa. *L* is typically :math:`\min(30, M)` for airstrafing and *M*
    for groundstrafing. *gamma1* is usually :math:`k_e \tau M A`.

    """
    speed = common.vec_length(v, 2)
    if common.float_zero(speed):
        raise ValueError('speed cannot be 0')
    vhat = v[:]
    common.vec_mul(vhat, 1 / speed, 2)
    ct = math.cos(theta)
    gamma2 = L - speed * ct
    if gamma2 <= 0.0:
        return
    st = math.sin(theta)
    mu = min(gamma1, gamma2)
    a = [vhat[0] * ct - vhat[1] * st, vhat[0] * st + vhat[1] * ct]
    common.vec_mul(a, mu, 2)
    common.vec_add(v, a, 2)
