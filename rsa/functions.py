import numpy as np


def get_random_prime_integer(bounds):
    for i in range(bounds.__len__() - 1):
        if bounds[i + 1] > bounds[i]:
            x = bounds[i] + np.random.randint(bounds[i + 1] - bounds[i])
            if is_prime(x):
                return x

        else:
            if is_prime(bounds[i]):
                return bounds[i]

        if is_prime(bounds[i + 1]):
            return bounds[i + 1]

    newBounds = [0 for i in range(2 * bounds.__len__() - 1)]
    newBounds[0] = bounds[0]
    for i in range(1, bounds.__len__()):
        newBounds[2 * i - 1] = int((bounds[i - 1] + bounds[i]) / 2)
        newBounds[2 * i] = bounds[i]

    return get_random_prime_integer(newBounds)


def is_prime(x):
    count = 0
    for i in range(int(x / 2)):
        if x % (i + 1) == 0:
            count = count + 1
    return count == 1


def pow_desc(exp: int, mod: int, message, debug=False):
    print(f'Titkosítjuk: a(z) {message} üzenetet {exp} kulccsal és {mod} modulóval')
    res = 1
    coefficient = 1
    base = message
    while exp > 1:
        if coefficient != 1:
            if debug:
                print(f'{message}^{exp} * {coefficient} ({mod}) = ')
        else:
            if debug:
                print(f'{message}^{exp} ({mod}) = ')

        if exp % 2 != 0:
            exp -= 1
            coefficient *= base
            if coefficient > mod:
                coefficient %= mod
            if debug: print(f'{message}^{exp} * {coefficient} ({mod}) = ')
            res = (res * message) % mod
        message = message ** 2
        if debug:
            print(f'{message}^{exp} * {coefficient} ({mod}) = ')
        message %= mod
        exp //= 2

    if coefficient != 1:
        if debug:
            print(f'{message}^{exp} * {coefficient} ({mod}) = ')
    else:
        if debug:
            print(f'{message}^{exp} ({mod}) = \n{exp & 1}')
    return (message * res) % mod


def euclidean_algorithm(a, b):
    if b == 0:
        return a
    print(f'{a} = {a // b}*{b} + {a % b}')
    return euclidean_algorithm(b, a % b)


def diophantine_equation(a, b, debug=False):
    if a == 0:
        return b, 0, 1
    if debug: print(f'Euklidészi a.: {a} = {a // b}*{b} + {a % b}')
    gcd, x1, y1 = diophantine_equation(b % a, a, debug)
    x = y1 - (b // a) * x1
    y = x1
    if debug: print(f'{gcd} = {y1}*{a} {x1} * {b}')
    return gcd, x, y
