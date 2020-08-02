import math

anglemod_u_rad = math.pi / 32768.0
anglemod_u_deg = 360.0 / 65536.0

def float_equal(a, b):
    """Test if a and b are equal, accounting for floating point errors."""
    return math.isclose(a, b)

def float_zero(a):
    """Test if a equals zero, a more tolerant version than
    :py:func:`float_equal(a, 0)`.
    """
    return math.isclose(a, 0, abs_tol=1e-6)

def vec_set(v, value, length=None):
    """Set every component of *v* to *value*."""
    if length is None:
        length = len(v)
    for i in range(length):
        v[i] = value

def vec_length(v, length=None):
    """Compute the norm of *v*."""
    if length is None:
        length = len(v)
    return math.sqrt(vec_dot(v, v, length))

def vec_normalize(v):
    """Normalize vector *v* in-place."""
    invnorm = 1.0 / vec_length(v, len(v))
    for i in range(len(v)):
        v[i] *= invnorm

def vec_dot(a, b, length=None):
    """Dot product of vectors *a* and *b*."""
    if length is None:
        length = len(a)
    return sum(a[i] * b[i] for i in range(length))

def vec_cross(a, b):
    """Cross product of vectors *a* and *b*."""
    return [a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0]]

def vec_add(a, b, length=None):
    """Add vectors *a* and *b* and store into *a*."""
    if length is None:
        length = len(a)
    for i in range(length):
        a[i] += b[i]

def vec_sub(a, b, length=None):
    """Subtract vectors *a* and *b* and store into *a*."""
    if length is None:
        length = len(a)
    for i in range(length):
        a[i] -= b[i]

def vec_mul(a, k, length=None):
    """Multiply vector *a* by a scalar *k* and store into *a*."""
    if length is None:
        length = len(a)
    for i in range(length):
        a[i] *= k

def anglemod_rad(a):
    """Radians version of the ``anglemod`` function in Half-Life."""
    return (int(a / anglemod_u_rad) & 0xffff) * anglemod_u_rad

def anglemod_deg(a):
    """Degrees version of the ``anglemod`` function in Half-Life."""
    return (int(a / anglemod_u_deg) & 0xffff) * anglemod_u_deg
