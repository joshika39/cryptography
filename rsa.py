import math
import math as m
import random
import numpy as np


def getRandomPrimeInteger(bounds):

    for i in range(bounds.__len__()-1):
        if bounds[i + 1] > bounds[i]:
            x = bounds[i] + np.random.randint(bounds[i+1]-bounds[i])
            if isPrime(x):
                return x

        else:
            if isPrime(bounds[i]):
                return bounds[i]

        if isPrime(bounds[i + 1]):
            return bounds[i + 1]

    newBounds = [0 for i in range(2*bounds.__len__() - 1)]
    newBounds[0] = bounds[0]
    for i in range(1, bounds.__len__()):
        newBounds[2*i-1] = int((bounds[i-1] + bounds[i])/2)
        newBounds[2*i] = bounds[i]

    return getRandomPrimeInteger(newBounds)


def isPrime(x):
    count = 0
    for i in range(int(x/2)):
        if x % (i+1) == 0:
            count = count+1
    return count == 1


def RSA_Public(N, t, message):
    print(f'Crypting: {message}^{t} mod {N}')
    res = 1
    coefficient = 1
    base = message
    while t > 1:
        if coefficient != 1:
            print(f'{message}^{t} * {coefficient} ({N}) = ')
        else:
            print(f'{message}^{t} ({N}) = ')

        if t % 2 != 0:
            t -= 1
            coefficient *= base
            if coefficient > N:
                coefficient %= N
            print(f'{message}^{t} * {coefficient} ({N}) = ')
            res = (res * message) % N
        message = message ** 2
        print(f'{message}^{t} * {coefficient} ({N}) = ')
        message %= N
        t //= 2

    if coefficient != 1:
            print(f'{message}^{t} * {coefficient} ({N}) = ')
    else:
        print(f'{message}^{t} ({N}) = \n{t & 1}')
    return (message * res) % N


def RSA_Secret(p, q, m, r):
    print("RSA Secret")
    N = p * q
    fi = (p - 1) * (q - 1)
    print(f'N is {N}, and fi is {fi}')
    return RSA_Public(N, m, r)


def calculateKeys(p, q, t):
    if t is not None:
        print(f'Prime numbers: ({p}, {q}). T is {t}')
    else:
        print(f'Prime numbers: ({p}, {q}).')

    fi = (p - 1) * (q - 1)
    m = -1
    while True:
        if t is None:
            t = random.randint(2, fi)
        print(f'T is {t}')

        if math.gcd(t, fi) == 1:
            i = 1
            while True:
                m = i
                # print(f'm is {i}, ({i} * {t} = {(i * t)}) mod {fi} is {(i * t) % fi}')
                if (m * t) % fi == 1:
                    # print(f'm is {m}')
                    return t, m
                i += 1
        else:
            t = random.randint(2, fi)


p1, q1 = getRandomPrimeInteger([1000, 10000]), getRandomPrimeInteger([1000, 10000])
t1, m1 = calculateKeys(p1, q1, None)
N1 = p1 * q1
print(f'Person1: p={p1}, q={q1}, t={t1} (prime: {isPrime(t1)}), m={m1}')
print(f'GCD of t and fi: {math.gcd(t1, (p1 - 1) * (q1 -1))}')

p2, q2 = getRandomPrimeInteger([1000, 10000]), getRandomPrimeInteger([1000, 10000])
t2, m2 = calculateKeys(p2, q2, None)
N2 = p2 * q2
print(f'Person2: p={p2}, q={q2}, t={t2} (prime: {isPrime(t2)}), m={m2}')
print(f'GCD of t and fi: {math.gcd(t2, (p2 - 1) * (q2 -1))}')


string = input(f'Enter a sentence: ')

tempNum = []
for char in string:
    tempNum.append(ord(char))


message = []
for i in range(len(tempNum)):
    send = tempNum[i]
    inital = RSA_Secret(p1, q1, m1, send)
    print(f'Encoded initial from {send} is {inital}')

    message.append(RSA_Public(N2, t2, inital))
    print(f'Encoded from {inital} is {message[i]}')
    print()
    print(message)

decoded = []
for i in range(len(message)):
    char = message[i]
    recieved = RSA_Secret(p2, q2, m2, char)
    print(f'Decoded test from {char} is {recieved}')

    decoded.append(RSA_Public(N1, t1, recieved))
    print(f'Decoded from {recieved} is {decoded[i]}')
    print()
    print(message)
    print(decoded)

for letter in decoded:
    print(chr(letter), end="")
