#! /bin/python3

import random
import time
import sys
import os


def block_print():
    # Disable
    sys.stdout = open(os.devnull, 'w')


def enable_print():
    # Restore
    sys.stdout = sys.__stdout__


def greatest_common_divisor(a, b):
    # ggT(a, b)
    #print(f'Calculating the greatest common divisor of {a}, {b} ...')
    r = 0
    if a == 0:
        return abs(b)
    if b == 0:
        return abs(a)
    while b != 0:
        r = a % b
        a = b
        b = r
    #print(f'Greatest common divisor: {abs(a)}')
    return abs(a)


def is_not_comparable(a, b):
    #print(f'Check if {a}, {b} are coprime to each other...')
    if greatest_common_divisor(a, b) == 1:
        #print(f'{a}, {b} are coprime to each other')
        return True
    else:
        # print(f'{a}, {b} are NOT coprime to each other')
        return False


def eulersche_phi(n):
    body = []
    phi = 0
    # print(f'Calculate the Body for n={n}')
    for i in range(n):
        if is_not_comparable(i, n):
            # phi(n) is the number of coprime numbers within the body of n
            # phi(n) = n - 1 if n i a prime number
            # phi(i * n) = phi(i) * phi(n), if ggT(i,n) = 1
            phi += 1
        body.append(i + 1)
    print(f'phi({n}) = {phi}')
    return phi


def fermats_little_theorem(a, exp, p):
    # fermats little theorem
    # source: https://www.youtube.com/watch?v=pMA-dD-KCWM
    # a^(p-1) = 1 mod p
    # exp = (p - 1) * x
    # divide the exp by (p -1) and get the reminder.
    x = int(exp / (p-1))
    r = exp % (p-1)
    print(f'Divide the exp = {exp} by ({p}-1) and get the reminder.')
    print(f'{exp} = {x} * {p-1} + {r}')
    # since we know a^(p-1) = 1, we now know that a^(p-1)^(x) = 1^(x) = 1
    # taking care of the reminder
    reminder = pow(a, r, p)
    print(f'{a} to the power of {exp} mod {p} equals: {reminder} mod {p}')


def extended_euclidean_algorithm(a, b):
    # source: https://www.inf-schule.de/kommunikation/kryptologie/rsa/modmultiplikation/station_berechnungmodinv
    aalt = a
    amitte = b
    xalt = 1
    xmitte = 0
    yalt = 0
    ymitte = 1
    while amitte != 0:
        q = aalt // amitte
        aneu = aalt - q * amitte
        xneu = xalt - xmitte * q
        yneu = yalt - ymitte * q
        xalt = xmitte
        xmitte = xneu
        yalt = ymitte
        ymitte = yneu
        aalt = amitte
        amitte = aneu
        print(f'{amitte} = {xmitte} * {a} + {ymitte} * {b}')
    return (aalt, xalt, yalt)


def mod_inv(a, m):
    # source https://www.inf-schule.de/kommunikation/kryptologie/rsa/modmultiplikation/station_berechnungmodinv
    (ggt, x, y) = extended_euclidean_algorithm(a, m)
    if ggt > 1:
        print(f'Inverse does not exists, ggT({a},{m}) > 1')
        return -1
    else:
        if x < 0:
            x = x + m
        return x


def multiplicative_inverse_modulo(a, m):
    # modulare multiplikative inverse
    _a = a
    _m = m
    r = 1
    equations = []
    if greatest_common_divisor(a, m) == 1:
        while r != 0:
            p = m//a
            r = m - (a * p)
            print(f'{m} = {a} * {p} + {r}')
            equations.append((m, a, p, r))
            m = a
            a = r
        print(f'Looking for inverse')
        res = mod_inv(_a, _m)
        print(f'Inverse for a={_a} and m={_m} is: {res}')
        return res
    else:
        print('Greatest common divisor is not 1')
        print('exit')
        return 0


def diffie_hellman_check(p, a):
    if a > (p - 2):
        print('alpha too big')
        return False

    for x in range(2, p):
        if p % x == 0:
            print(f'p = {p} is not a prime number')
            return False
    return True


def diffie_hellman(p, alpha):
    if diffie_hellman_check(p, alpha):
        print(f'[Public]Selected Domain Parameter: p = {p}, alpha = {alpha}')

    a = random.randint(2, (p-2))
    print(f'[Alice (private)] a = k_pr,A = {a}')
    b = random.randint(2, (p-2))
    print(f'[Bob (private)] b = k_pr,B = {b}')

    A = pow(alpha, a) % p
    B = pow(alpha, b) % p
    print(f'A = k_pub,A = alpha^a = {A}')
    print(f'B = k_pub,B = alpha^b = {B}')
    print(f'Alice --- {A} ----> Bob')
    print(f'Alice <---- {B} --- Bob')

    print(f'k_AB = B^a mod p = {pow(B, a) % p}')
    print(f'k_BA = A^b mod p = {pow(A, b) % p}')


def RSA(p, q, e=0):
    print('Basic principal is a big number, decomposed in its prime factors')
    print('and the decomposition into prime factors')
    print('Key Generation')
    print('Each participant chooses two random prime factors p and q and chooses the numbers e and d as follows:')
    n = p * q
    print(f'n = p * q = {p} * {q} = {n}')
    print(f'phi(n) = phi({n}) = (p - 1) * (q - 1) = {(p - 1) * (q - 1)}')
    phi = eulersche_phi(n)
    print(f'Choose a small odd number e between 1 < e < phi(n) and ggT(e, phi(n)) == 1')
    if e == 0:
        e = 0
        for possible_e in range(2, phi):
            # is possible_e odd?
            if possible_e % 2 != 0:
                if greatest_common_divisor(possible_e, phi) == 1:
                    e = possible_e
                    print(f'e = {e}')
                    break

    print('d is a number: 1 < d < phi(n) and e*d = 1 mod phi(n)')
    d = multiplicative_inverse_modulo(e, phi)
    if d > 0:
        print(f'd = {d}')
        print('----------------------------------')
        print(f'Public Key (e, n): ({e}, {n})')
        print(f'Private Key d: {d}')
    else:
        print(f'Keypair for p = {p}, q = {q} does not exist')

    public = (n, e)
    private = d
    return public, private


def message_RSA(num, p, q, e=0):
    #block_print()
    start = time.time_ns()
    if e != 0:
        (n, e), private = RSA(p, q, e)
    else:
        (n, e), private = RSA(p, q)
    if num >= n:
        #enable_print()
        print(f'given number too big. Must be smaller than {n}')
        return
    chiffre = pow(num, e) % n
    cleartext = pow(chiffre, private) % n
    end = time.time_ns()
    #enable_print()
    print(f'Message: {num}')
    print(f'Encrypted {chiffre}')
    print(f'Decrypted {cleartext}')
    print(f'Total time: {round(round(end - start) / 1000000, 2)} ms')


if __name__ == '__main__':

    # message_RSA(10, 61, 97, 47)
    # multiplicative_inverse_modulo(7, 40)
    RSA(5, 11, 7)
    # diffie_hellman(17, 4)
    # greatest_common_divisor(13, 7)
    # fermats_little_theorem(10, 99, 9)

