"""Mathematical routines for player motion under gravity.

Typically you would want to compute ``K`` using the ``strafe_K`` function, which
is needed by many of the functions in this module.

Consult the Half-Life physics documentation at https://www.jwchong.com/hl/.
"""

import math
import scipy.optimize as opt
from pystrafe import common

def strafe_K(L, tau, M, A):
    """Compute K based on strafing parameters.

    This function will not deal with case 3 strafing where L - tau MA > speed,
    which occurs when the speed is sufficiently small. The user is responsible
    of verifying this assumption. Consequently, this function also does not
    accept negative parameters, which may give rise to case 3 strafing.

    >>> strafe_K(30, 0.001, 320, 10)
    181760.0
    """
    if L < 0 or tau < 0 or M < 0 or A < 0:
        raise ValueError('parameters must be > 0')
    L = min(L, M)
    LtauMA = L - tau * M * A
    if LtauMA <= 0:
        return L * L / tau
    return M * A * (L + LtauMA)

def strafe_speedxf(t, speed, K):
    """Compute the speed after strafing for t seconds.

    Assumes case 1 or case 2 strafing, and does not handle edge cases present in
    the game when the speed is very small.

    >>> K = 320 * 10 * (60 - 0.001 * 320 * 10)
    >>> '{:.10g}'.format(strafe_speedxf(2, 320, K))
    '682.5833282'

    >>> K = 900 / 0.01
    >>> '{:.10g}'.format(strafe_speedxf(3.5, 10, K))
    '561.337688'

    >>> strafe_speedxf(338.13, 387.4, 0)
    387.4
    >>> strafe_speedxf(0, 505, 505)
    505.0
    """
    if K < 0:
        raise ValueError('K must be > 0')
    return math.sqrt(speed * speed + t * K)

def strafe_distance(t, speed, K):
    """Compute the distance after strafing for t seconds.

    Assumes case 1 or case 2 strafing, and does not handle edge cases present in
    the game when the speed is very small. In addition, this is a continuous
    time approximation to the true distance a player would have travelled in
    Half-Life. Nevertheless, the approximation is good even at lower frame rates
    and is rarely a concern.

    >>> K = 320 * 10 * (60 - 0.001 * 320 * 10)
    >>> '{:.10g}'.format(strafe_distance(2.5, 400, K))
    '1531.650819'
    >>> '{:.10g}'.format(strafe_distance(1.3, 0, K))
    '421.2820222'
    >>> strafe_distance(0, 5000, K)
    0.0
    >>> strafe_distance(5000, 5000, 0)
    25000000.0
    """
    if K < 0:
        raise ValueError('K must be > 0')
    speed = math.fabs(speed)
    if common.float_equal(K, 0.0):
        return speed * t
    speedsq = speed * speed
    ret = ((speedsq + t * K) ** 1.5 - speedsq * speed) / (1.5 * K)
    if isinstance(ret, complex):
        raise ValueError('math domain error')
    return math.fabs(ret)

def strafe_time(x, speedxi, K):
    """Compute the time it takes to strafe for the given distance and initial
    speed.

    Always returns positive times.

    >>> vix = 400
    >>> x = 1000
    >>> K = strafe_K(30, 0.01, 320, 10)
    >>> tx = strafe_time(x, vix, K)
    >>> math.isclose(x, strafe_distance(tx, vix, K))
    True
    """
    if K < 0:
        raise ValueError('K must be > 0')
    speedxi = math.fabs(speedxi)
    x = math.fabs(x)
    if common.float_zero(x):
        return 0.0
    if common.float_zero(K):
        try:
            return x / speedxi
        except ZeroDivisionError:
            return math.inf
    sq = speedxi * speedxi
    ret = ((sq * speedxi + 1.5 * K * x) ** (2 / 3) - sq) / K
    # ret < 0 can occur from the subtraction with small x and big speedxi
    return max(ret, 0.0)

def gravity_speediz_distance_time(t, z, g):
    """Compute the initial speed need to travel to the given ``z`` position.

    z can be negative.
    """
    if common.float_zero(t) and common.float_zero(z):
        raise ValueError('indeterminate')
    try:
        return (0.5 * g * t * t + z) / t
    except ZeroDivisionError:
        return math.copysign(math.inf, z)

def gravity_time_speediz_z(speedzi, z, g):
    """Compute the time it takes for to reach a height given initial vertical
    velocity.

    z can be negative.

    >>> viz = 200
    >>> z = 10
    >>> g = 800
    >>> t1, t2 = gravity_time_speediz_z(viz, z, g)
    >>> '{:.10g} {:.10g}'.format(t1, t2)
    '0.05635083269 0.4436491673'
    >>> math.isclose(z, viz * t1 - 0.5 * g * t1 * t1)
    True
    >>> math.isclose(z, viz * t2 - 0.5 * g * t2 * t2)
    True
    """
    if common.float_zero(g):
        t = z / speedzi
        return t, t
    sqrt_tmp = math.sqrt(speedzi * speedzi - 2 * g * z)
    t1 = (speedzi - sqrt_tmp) / g
    t2 = (speedzi + sqrt_tmp) / g
    return t1, t2

def strafe_solve_speedxi(speedzi, K, x, z, g):
    """Compute the initial horizontal speed needed to reach the final position.

    z can be negative.

    Automatically handles both cases where the final velocity is positive or
    negative.

    If the time it takes to reach the vertical position is longer or equal to
    the *maximum* time it takes the reach the horizontal position (calculated by
    setting the initial horizontal speed to zero), the function will simply
    return 0.0, indicating that strafing from zero speed is enough to reach the
    final horizontal position *sooner than required*. In such a case, the user
    needs to manually "slow down" the strafing, by taking a longer path in 3-d
    space, stop strafing altogether at some point, or "backpedalling" in air, so
    that both the horizontal and vertical positions can hit the final position
    exactly at the same time. In other words, the user must "wait" for the
    vertical position to move up to the final position before the horizontal
    position should hit it.

    The result is computed using the ``brentq`` function provided by scipy.
    """
    if K < 0:
        raise ValueError('K must be > 0')

    sqrt_tmp = math.sqrt(speedzi * speedzi - 2 * g * z)
    tz = speedzi - sqrt_tmp
    if tz < 0:
        tz = speedzi + sqrt_tmp
    if tz < 0:
        return math.nan
    tz /= g

    x = math.fabs(x)
    txmax = (1.5 * x) ** (2 / 3) * K ** (-1 / 3)
    if common.float_zero(txmax):
        return 0.0

    if common.float_equal(txmax, tz) or txmax < tz:
        return 0.0
    elif common.float_zero(tz):
        return math.inf

    # The upper bound of x / tz is the minimum _constant_ speed needed
    tmp = 1.5 * K * x
    return opt.brentq(
        lambda v: ((v ** 3 + tmp) ** (2 / 3) - v ** 2) / K - tz, 0, x / tz)

def solve_boost_min_dmg(vi, K, x, z, g):
    """Compute the speed boost that minimises health loss.

    The minimisation is done using the ``minimize_scalar`` function provided by
    scipy running the Brent's algorithm.

    The resulting curve tends to end with a negative vertical velocity.

    >>> vi = [100, 268]
    >>> K = strafe_K(30, 0.001, 320, 10)
    >>> x, z = 400, 500
    >>> g = 800
    >>> dv = solve_boost_min_dmg(vi, K, x, z, g)
    >>> '{:.5g} {:.5g}'.format(dv[0], dv[1])
    '27.394 627.83'
    >>> tz1, tz2 = gravity_time_speediz_z(vi[1] + dv[1], z, g)
    >>> tx = strafe_time(x, vi[0] + dv[0], K)
    >>> math.isclose(tz2, tx)
    True
    >>> vi[1] + dv[1] - g * tz2 < 0
    True
    """
    if K < 0:
        raise ValueError('K must be > 0')

    def compute_dy(dx):
        tx = strafe_time(x, vix + dx, K)
        try:
            dy = gravity_speediz_distance_time(tx, z, g) - vi[1]
        except ValueError:
            dy = 0.0
        return max(dy, 0.0)

    def fun(dx):
        dy = compute_dy(dx)
        return dx * dx + dy * dy

    x = math.fabs(x)
    vix = math.fabs(vi[0])
    res = opt.minimize_scalar(fun)
    dx = max(res.x, 0.0)
    dy = compute_dy(dx)
    return [dx, dy]
