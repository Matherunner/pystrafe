import math

def friction(speed, tau, E, k):
    if speed >= E:
        return speed - speed * tau * k
    else:
        return max(speed - E * k * tau, 0)

def strafe_maxaccel(speed, L, tau, M, A, E, k):
    speed = friction(speed, tau, E, k)
    tauMA = tau * M * A
    LtauMA = L - tauMA
    if LtauMA <= 0:
        return math.sqrt(speed * speed + L * L)
    elif LtauMA <= speed:
        return math.sqrt(speed * speed + tauMA * (L + LtauMA))
    else:
        return speed + tauMA
