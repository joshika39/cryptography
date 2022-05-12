import math
import math as m
import random
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


def pow_desc(exp: int, mod: int, message):
    print(f'Crypting: {message}^{exp} mod {mod}')
    res = 1
    coefficient = 1
    base = message
    while exp > 1:
        if coefficient != 1:
            print(f'{message}^{exp} * {coefficient} ({mod}) = ')
        else:
            print(f'{message}^{exp} ({mod}) = ')

        if exp % 2 != 0:
            exp -= 1
            coefficient *= base
            if coefficient > mod:
                coefficient %= mod
            print(f'{message}^{exp} * {coefficient} ({mod}) = ')
            res = (res * message) % mod
        message = message ** 2
        print(f'{message}^{exp} * {coefficient} ({mod}) = ')
        message %= mod
        exp //= 2

    if coefficient != 1:
        print(f'{message}^{exp} * {coefficient} ({mod}) = ')
    else:
        print(f'{message}^{exp} ({mod}) = \n{exp & 1}')
    return (message * res) % mod


class Key:
    def __init__(self, p: int = 0, q: int = 0, e: int = 0):
        if p != 0 or q != 0 or e != 0:
            self.p, self.q = p, q
            self.n = self.p * self.q
            self.fi = (self.p - 1) * (self.q - 1)
            self.e = e
            if math.gcd(self.e, self.fi) != 1:
                print("Nem jo, nyilt kulcs.. Keresek en!")
                self._get_public_key()
            self._get_private_key()
        else:
            limits = [800, 1000]
            self.p, self.q = get_random_prime_integer(limits), get_random_prime_integer(limits)
            while self.p == self.q:
                self.p, self.q = get_random_prime_integer(limits), get_random_prime_integer(limits)
            self.n = self.p * self.q
            self.fi = (self.p - 1) * (self.q - 1)
            self._get_public_key()
            self._get_private_key()

    def _get_public_key(self):
        self.e = random.randint(2, self.fi)
        print(f'e: {self.e}, fi: {self.fi}')
        gcd = math.gcd(self.e, self.fi)
        print(f'GCD: {gcd}, e: {self.e}, fi: {self.fi}')
        if gcd != 1:
            while gcd != 1:
                self.e = random.randint(2, self.fi)
                gcd = math.gcd(self.e, self.fi)
                print(f'GCD: {gcd}, e: {self.e}, fi: {self.fi}')

    def _get_private_key(self):
        gcd, a, b = self._gcd_extended(self.e, self.fi)
        print(f'private key: {self.fi} + {a}')
        if a > 0:
            self.t = a
        else:
            self.t = self.fi + a

    def _gcd_extended(self, a, b):
        print(f'pre, a: {a}, b: {b}')
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = self._gcd_extended(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        print(f'gcd: {gcd}, x: {x}, y: {y}')
        return gcd, x, y


class Person:
    def __init__(self, key: Key = None, name: str = None, debug=False):
        if name is None:
            self.name = input("A szemely neve: ")
        else:
            self.name = name
        self.proba = debug
        if key is None:
            if self.proba:
                p = int(input("1. Prim szam: "))
                q = int(input("2. Prim szam: "))
                e = int(input("Nyilt kulcs: "))
                self._key = Key(p, q, e)
            else:
                self._key = Key()
        else:
            self._key = key

    def share_pub_key(self) -> tuple[int, int]:
        return self._key.e, self._key.n

    def print_all_data(self):
        t_key = self._key
        print(f'{self.name} primjei: {t_key.p} es {t_key.q}')
        print(f'{self.name} modulusa: {t_key.n} es fi-je: {t_key.fi}')
        print(f'{self.name} nyilt kulcsa: {t_key.e} es titkos kulcsa: {t_key.t}')

    def send_message_to(self, foreign_key: tuple[int, int], text: int, self_coded=False) -> int:
        f_e, f_n = foreign_key
        if not self_coded:
            return pow_desc(f_e, f_n, text)
        else:
            print(f"Az en ({self.name.lower()}) titkoskulcsom rarakasa")
            init_layer = pow_desc(self._key.t, self._key.n, text)
            print("Az idegen nyiltkulcs rarakasa")
            final_layer = pow_desc(f_e, f_n, init_layer)
            return final_layer

    def receive_message(self, foreign_key: tuple[int, int], text: int, self_coded=False) -> int:
        f_e, f_n = foreign_key
        if not self_coded:
            return pow_desc(self._key.t, self._key.n, text)
        else:
            print(f"Az en ({self.name.upper()}) nyiltkulcsom lebontasa")
            init_layer = pow_desc(self._key.t, self._key.n, text)
            print("Az idegen titkoskulcs lebontasa")
            final_layer = pow_desc(f_e, f_n, init_layer)
            return final_layer


proba = bool(input("Proba? (True, False)"))
person_1 = Person(Key(7, 11, 13), name="J")
person_2 = Person(Key(5, 19, 7), "Z")
person_1.print_all_data()
person_2.print_all_data()
send = 8
en_message = person_1.send_message_to(person_2.share_pub_key(), send, True)
print(f'Message: {send}, encrypted: {en_message}')
print()
de_message = person_2.receive_message(person_1.share_pub_key(), en_message, True)
print(f'Encrypted: {en_message}, decrypted: {de_message}')
