def gf_mod(a, b):
    while a.bit_length() >= b.bit_length():
        a = a ^ (b << a.bit_length()-b.bit_length())

    return a


def bin_mult(a, b):
    product = 0

    if a == 1:
        product = b

    else:    
        while a != 0:
            product = product ^ (b << a.bit_length() - 1)
            a = a ^ (1 << (a.bit_length() - 1))

    return product


def gf_mult(a, b):
    product = bin_mult(a, b)
    product = gf_mod(product, 283)

    return product


def bin_div(a, b):
    quotient = 0

    if a.bit_length() == b.bit_length():
        quotient = 1

    elif a.bit_length() > b.bit_length():
        quotient = 0

    elif a.bit_length() < b.bit_length():
        while a.bit_length() < b.bit_length() + 1:
            quotient = quotient ^ 1 << (b.bit_length() - a.bit_length())
            b = b ^ (a << (b.bit_length() - a.bit_length()))

        if a.bit_length() == b.bit_length():
            quotient = quotient ^ 1

    return quotient


def euclid(a, b):
    r_2, r_i, r_k = a, b, 0

    q = r_2 / r_1
    r_k = r_2 % r_1

    while r_k != 0:
        r_2 = r_1
        r_1 = r_k
        q = r_2 / r_1
        r_k = r_2 % r_1

    return r_1


def extended_euclid(a, b):
    r_i, r_2, r_1 = 0, a, b
    t_i, t_2, t_1 = 0, 0, 1

    quotient = bin_div(r_1, r_2)
    r_i = r_2 ^ bin_mult(r_1, quotient)
    t_i = t_2 ^ bin_mult(t_1, quotient)

    while r_2 ^ bin_mult(r_1, quotient) != 0:
        r_2 = r_1
        r_1 = r_i
        t_2 = t_1
        t_1 = t_i
        quotient = bin_div(r_1, r_2)
        r_i = r_2 ^ bin_mult(r_1, quotient)
        t_i = t_2 ^ bin_mult(t_1, quotient)

    return t_1


def multiplicative_inverse(a):
    if a == 0:
        inverse = 0
    
    else:
        inverse = extended_euclid(283, a)

    return inverse


def affine_transformation(b):
    b0, b1, b2, b3, b4, b5, b6, b7 = 0, 0, 0, 0, 0, 0, 0, 0
    output = 0

    if b > b ^ 1:
        b0 = 1
    if b > b ^ 2:
        b1 = 1
    if b > b ^ 4:
        b2 = 1
    if b > b ^ 8:
        b3 = 1
    if b > b ^ 16:
        b4 = 1
    if b > b ^ 32:
        b5 = 1
    if b > b ^ 64:
        b6 = 1
    if b > b ^ 128:
        b7 = 1

    bp0 = b0 ^ b4 ^ b5 ^ b6 ^ b7 ^ 1
    bp1 = b1 ^ b5 ^ b6 ^ b7 ^ b0 ^ 1
    bp2 = b2 ^ b6 ^ b7 ^ b0 ^ b1 ^ 0
    bp3 = b3 ^ b7 ^ b0 ^ b1 ^ b2 ^ 0
    bp4 = b4 ^ b0 ^ b1 ^ b2 ^ b3 ^ 0
    bp5 = b5 ^ b1 ^ b2 ^ b3 ^ b4 ^ 1
    bp6 = b6 ^ b2 ^ b3 ^ b4 ^ b5 ^ 1
    bp7 = b7 ^ b3 ^ b4 ^ b5 ^ b6 ^ 0

    output = bp0 ^ (bp1 << 1) ^ (bp2 << 2) ^ (bp3 << 3) ^ (bp4 << 4) ^ (bp5 << 5) ^ \
            (bp6 << 6) ^ (bp7 << 7)

    return output