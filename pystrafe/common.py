import math

def float_equal(a, b):
    """Test if a and b are equal, accounting for floating point errors."""
    return math.isclose(a, b)

def float_zero(a):
    """Test if a equals zero, a more tolerant version than
    :py:func:`float_equal(a, 0)`.
    """
    return math.isclose(a, 0, abs_tol=1e-6)

def vec_length(v, length):
    """Compute the norm of *v*."""
    return math.sqrt(vec_dot(v, v, length))

def vec_normalize(v):
    """Normalize vector *v*."""
    invnorm = 1.0 / vec_length(v, len(v))
    for i in range(len(v)):
        v[i] *= invnorm

def vec_dot(a, b, length):
    """Dot product of vectors *a* and *b*."""
    return sum(a[i] * b[i] for i in range(length))

def vec_cross(a, b):
    """Cross product of vectors *a* and *b*."""
    return [a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0]]

def vec_add(a, b):
    """Add vectors *a* and *b*."""
    for i in range(len(a)):
        a[i] += b[i]

def vec_sub(a, b):
    """Subtract vectors *a* and *b*."""
    for i in range(len(a)):
        a[i] -= b[i]

def vec_mul(a, k):
    """Multiply vector *a* by a scalar *k*."""
    for i in range(len(a)):
        a[i] *= k
