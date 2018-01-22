import math

def float_equal(a, b):
    return math.isclose(a, b)

def float_zero(a):
    return math.isclose(a, 0, abs_tol=1e-6)

def vec_length(v, length):
    return math.sqrt(sum(v[i] * v[i] for i in range(length)))

def vec_normalize(v):
    invnorm = 1.0 / vec_length(v)
    for i in range(len(v)):
        v[i] *= norm

def vec_dot(a, b, length):
    return sum(a[i] * b[i] for i in range(length))

def vec_cross(a, b):
    return [a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0]]
