"""Routines to compute the optimal viewangles for climbing ladders.
"""

import math
from pystrafe import common

def climb_velocity(n, f, s):
    """Compute the climbing velocity given unit acceleration vectors.
    """
    if math.isclose(math.fabs(n[2]), 1):
        return

    u = [f[0] + s[0], f[1] + s[1], f[2] + s[2]]
    tmp = common.vec_cross(n, [0, 0, 1])
    fac = common.vec_cross(n, tmp)
    fac /= common.vec_length(tmp, 3)
    fac = [fac[0] + n[0], fac[1] + n[1], fac[2] + n[2]]
    fac *= common.vec_dot(u, n, 3)
    return [u[0] - fac[0], u[1] - fac[1], u[2] - fac[2]]

def maxspeed_normal(n, vdir, F, S):
    """Compute the viewwangles for climbing a ladder at maximum speed.
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
