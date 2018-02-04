"""Functions related to the health and damage system in Half-Life.
"""

import math
from pystrafe import common

def hpap_damage(hp, ap, dmg):
    """Compute the new HP and AP given damage.

    The damage can be negative.

    This function works for all damage types except ``DMG_FALL`` and
    ``DMG_DROWN``, both of which bypass the armour. The health loss due to these
    types of damage is simply the truncated damage value.

    >>> hpap_damage(100, 100, 100)
    (80, 60.0)
    >>> hpap_damage(100, 0, 50.5)
    (50, 0.0)

    Negative damages are accepted, such as the damage from the infinite health
    doors in the Half-Life main campaign:

    >>> hpap_damage(100, 0, -1)
    (101, 0.0)
    """
    new_ap = 0.0 if common.float_zero(ap) else max(0.0, ap - 0.4 * dmg)
    hp -= int(dmg - 2 * ap if common.float_zero(new_ap) else 0.2 * dmg)
    return hp, new_ap

#def boost_dhp(dhp, r, infr):
#    """Compute the delta-v resulting from the health loss.
#
#    All vectors are 3D.
#    """
#    d = [r[0] - infr[0], r[1] - infr[1], r[2] - infr[2] + 10]
#    pass

def ap_dhp_damage(dhp, dmg):
    """Compute the AP needed to achieve the desired HP loss from the given
    damage.

    The input health loss *dhp* is always truncated before computations.
    Negative *dhp* and/or *dmg* are accepted. Note that some combinations of
    *dhp* and *dmg* do not admit a solution.

    Return a 4-tuple (*apl*, *apu*, *bl*, *bu*), where *apl* and *apu* form an
    interval, and the specific meaning of these values depends on the strings
    *bl* and *bu*.

    *apl* always refers to the lower bound of the amount of AP. If *bl* is
    ``'('``, then this lower point is not included in the interval. If *bl* is
    ``'['``, then this lower point is included. If *bl* is ``None``, then *apl*
    will be ``NaN`` and therefore there is no solution to the given input.

    *apu* refers to the upper bound of the amount of AP if *bu* is ``')'`` or
    ``']'``. That is, if *bu* is ``')'``, then this upper point is not included.
    If *bu* is ``']'``, then this upper point is included. If *bu* is ``'inf'``,
    then this is the *inclusive* upper bound such that the final AP would be
    zero given *dmg*. In other words, if the AP is set to be higher than *apu*,
    the same *dmg* would still result in the desired HP loss, except that the
    final AP would be nonzero. For example,

    >>> ap_dhp_damage(1, 8)
    (3.0, 3.2, '(', 'inf')

    If we apply the same *dmg* of 8 but with 3.2 AP, we obtain a health loss of
    1 (reduced from 100 down to 99 in this case) and 0 AP as expected:

    >>> hpap_damage(100, 3.2, 8)
    (99, 0.0)

    But if we increase the AP amount beyond 3.2, then we will get a nonzero AP.

    >>> hpap_damage(100, 3.7, 8)
    (99, 0.5)
    >>> hpap_damage(100, 3.20001, 8) != (99, 0.0)
    True

    If *bu* is ``None``, then *apu* will be ``NaN`` and therefore there is no
    solution to the given input.

    Note that inputting a value of 0 for *dmg* implies a damage is still taken,
    albeit with a value of zero. This distinction is significant when negative
    armour values are returned.
    """
    dhp = int(dhp)
    if dhp < 0:
        if math.isclose(dmg, dhp):
            return (0.0, 0.0, '[', ']')
        if dmg > 5 * dhp:
            return math.nan, math.nan, None, None
        apl = 0.5 * (dmg - dhp)
        interval = ('[', ')' if dmg <= 5 * (dhp - 1) else 'inf')
    else:
        if dmg >= 5 * (dhp + 1):
            return math.nan, math.nan, None, None
        apl = 0.5 * (dmg - dhp - 1)
        interval = ('(', ']' if dmg < 5 * dhp else 'inf')

    max_ap = 0.4 * dmg
    apu = apl + 0.5
    return (apl, min(apu, max_ap), *interval)

def fall(vfz):
    """Compute the fall damage inflicted given final vertical speed on touch.

    Return the untruncated damage corresponding to touch-ground vertical speed
    *vfz*. Only positive *vfz* values are meaningful.
    """
    return max(0.0, 25 * (vfz - 580) / 111)

#def radius_falloff():
#    pass
#
#def hp_distrib(hp, xs):
#    pass
