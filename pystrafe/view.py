"""Routines related to player's camera views."""

import math
import warnings
from pystrafe import common

def angles_to_vectors(pitch, yaw, dim):
    """Convert pitch and yaw to view vectors.

    Angles must be in radians, and the roll is assumed to be zero. *dim*
    specifies the dimensions of pitch and yaw, and can be either ``2`` or ``3``.
    In the 2D case, this function is equivalent to computing the 3D vectors,
    discarding the *z* component, and then normalising only the *x* and *y*
    components.

    Returns a 2-tuple (*fv*, *sv*), where *fv* is the unit forward view vector
    and *sv* is the unit side view vector.

    >>> fv, sv = angles_to_vectors(0, math.pi / 4, 2)
    >>> f'{fv[0]:.6g} {fv[1]:.6g}'
    '0.707107 0.707107'
    >>> f'{sv[0]:.6g} {sv[1]:.6g}'
    '0.707107 -0.707107'

    Note that the phenomenon of gimbal lock can occur in the two dimensional
    output when the pitch is 90 degrees up or down, thus losing directionality
    in the horizontal plane. A warning will be issued when this happens. This is
    because when the pitch is 90 degrees up or down, the *x* and *y* components
    of *fv* will both be zero, thus normalising them would be indeterminate. In
    the implementation of this function, the *fv* and *sv* vectors would still
    be computed as though the pitch is not vertical, but they may not behave
    correctly in game or other algorithms based on normalising the horizontal
    components of the 3D vectors.
    """
    syaw, cyaw = math.sin(yaw), math.cos(yaw)
    spitch, cpitch = math.sin(pitch), math.cos(pitch)
    if dim == 2:
        sv = [syaw, -cyaw]
        fv = [cyaw, syaw]
        if common.float_zero(cpitch):
            warnings.warn('gimbal lock due to pitch of +/- pi/2', RuntimeWarning)
    elif dim == 3:
        sv = [syaw, -cyaw, 0.0]
        fv = [cyaw * cpitch, syaw * cpitch, -spitch]
    else:
        raise ValueError('dim must be either 2 or 3')
    return fv, sv
