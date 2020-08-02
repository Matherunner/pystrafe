"""Routines to compute the optimal viewangles for climbing ladders.
"""

import math
from pystrafe import common

def climb_velocity(n, f, s, F, S):
    """Compute the climbing velocity given unit acceleration vectors.

    Parameters *n*, *f*, and *s* are 3D vectors. *n* is the unit normal of the
    climbing surface. There is no restriction on the directionality of *n*. *f*
    is the unit forward acceleration of the player, while *s* is the unit side
    acceleration of the player.

    *F* and *S* can be either positive, negative, or zero. Only the sign is
    considered. Positive *F* means ``+forward`` is held down, while negative *F*
    means ``+back`` is held down. Positive *S* means ``+moveright`` is held
    down, while negative *S* means ``+moveleft`` is held down.

    Return the player climbing velocity in 3D.
    """
    if not common.float_equal(common.vec_dot(n, n, 3), 1):
        raise ValueError('n must be a unit vector')
    if not common.float_equal(common.vec_dot(f, f, 3), 1):
        raise ValueError('f must be a unit vector')
    if not common.float_equal(common.vec_dot(s, s, 3), 1):
        raise ValueError('s must be a unit vector')

    f, s = f[:], s[:]
    common.vec_mul(f, 0 if common.float_zero(F) else math.copysign(200, F))
    common.vec_mul(s, 0 if common.float_zero(S) else math.copysign(200, S))

    u = [0.0, 0.0, 0.0]
    common.vec_add(u, f)
    common.vec_add(u, s)
    cross = common.vec_cross([0, 0, 1], n)
    cross_norm = common.vec_dot(cross, cross)
    if common.float_zero(cross_norm):
        fac = [0.0, 0.0, 0.0]
    else:
        fac = common.vec_cross(n, cross)
        common.vec_mul(fac, 1 / cross_norm)
    common.vec_add(fac, n)
    common.vec_mul(fac, common.vec_dot(u, n))
    common.vec_sub(u, fac)
    return u

def maxspeed_normal(n, vdir, F, S):
    """Compute the viewwangles for climbing a ladder at maximum speed.

    *n* is the unit ladder normal. The sign of *vdir* represents the desired
    vertical direction, where positive indicates up and negative indicates down.
    The sign of *F* and *S* have the same meaning as those in the
    :py:meth:`climb_speed` function, except they cannot be set to zero.

    Return a 2-tuple (*pitch*, *yaw*) representing the optimal viewangles for
    climbing this ladder at maximum speed. If the ladder is horizontal, then
    *yaw* is ``None`` as its value is indetermine and depends on the desired
    horizontal direction to move towards. The desired direction cannot be
    deduced from the input arguments. Consult the `Half-Life Physics Reference`_
    for more information.

    .. _Half-Life Physics Reference: https://www.jwchong.com/hl/
    """
    if not math.isclose(common.vec_dot(n, n, 3), 1):
        raise ValueError('n must be a unit vector')

    if math.isclose(math.fabs(n[2]), 1):
        return 0.0, None

    sign_vdir = math.copysign(1, vdir)
    sign_F = math.copysign(1, F) * sign_vdir
    sign_S = math.copysign(1, S) * sign_vdir
    yaw = math.atan2(n[1], n[0])

    if n[2] >= 0:
        tmp = math.sqrt(2 * n[2] * math.hypot(n[0], n[1]))
        yaw += math.atan2(-sign_S, -sign_F * tmp)
        sign_nzdiff = math.copysign(1, math.sqrt(0.5) - n[2])
        pitch = -sign_F * sign_nzdiff * math.acos(tmp)
    else:
        sign_nzadd = math.copysign(1, math.sqrt(0.5) + n[2])
        yaw += sign_S * sign_nzadd * 0.5 * math.pi
        pitch = -sign_F * 0.5 * math.pi

    return pitch, yaw
