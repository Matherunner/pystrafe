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

def boost_dhp(dhp, r, infr):
    """Compute the delta-v resulting from the health loss.

    All vectors are 3D.
    """
    d = [r[0] - infr[0], r[1] - infr[1], r[2] - infr[2] + 10]
    pass

def ap_dhp_damage(dhp, dmg):
    """Compute the AP needed to achieve the desired HP loss from the given
    damage.

    The health loss is truncated to an integer. Note that inputting a value of 0
    for ``dmg`` implies a damage is still taken, albeit with a damage value of
    zero. This distinction is significant when negative armour values are
    returned.

    TODO: talk about return values

    When ``t2`` is ``inf``, then ``ub`` indicates the maximum value of AP that
    will result in zero AP after damage. The upper bound in this case always
    includes the end point (i.e. implicit type ``]``). Any value of AP above
    this upper bound will still result in the same health loss, but there would
    be nonzero AP left after the damage.
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
    """
    return max(0.0, 25 * (vfz - 580) / 111)

def radius_falloff():
    pass

def hp_distrib(hp, xs):
    pass
