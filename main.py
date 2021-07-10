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


def greatest_common_divisor(a, b, out=True):
    # ggT(a, b)
    print(f'Calculating the greatest common divisor of {a}, {b} ...')
    if not out:
        block_print()
    r = 0
    if a == 0:
        return abs(b)
    if b == 0:
        return abs(a)
    print(f'{b} = {int(b / a)} * {a} + {b - a * int(b / a)}')
    while b != 0:
        r = a % b
        a = b
        b = r
        try:
            print(f'{b} = {int(a / b) } * {b} + {a % b}')
        except BaseException as err:
            pass
    if not out:
        enable_print()
    print(f'Greatest common divisor: {abs(a)}')
    return abs(a)


def is_not_comparable(a, b):
    # print(f'Check if {a}, {b} are coprime to each other...')

    if greatest_common_divisor(a, b) == 1:
        # print(f'{a}, {b} are coprime to each other')
        return True
    else:
        # print(f'{a}, {b} are NOT coprime to each other')
        return False


def eulersche_phi(n):
    body = []
    phi = 0
    # print(f'Calculate the Body for n={n}')
    block_print()
    for i in range(n):
        if is_not_comparable(i, n):
            # phi(n) is the number of coprime numbers within the body of n
            # phi(n) = n - 1 if n i a prime number
            # phi(i * n) = phi(i) * phi(n), if ggT(i,n) = 1
            phi += 1
        body.append(i + 1)
    enable_print()
    print(f'phi({n}) = {phi}')
    return phi


def fermats_little_theorem(a, exp, p):
    # fermats little theorem
    # source: https://www.youtube.com/watch?v=pMA-dD-KCWM
    # a^(p-1) = 1 mod p
    # exp = (p - 1) * x
    # divide the exp by (p -1) and get the reminder.
    x = int(exp / (p - 1))
    r = exp % (p - 1)
    print(f'Divide the exp = {exp} // ({p}-1) = {x} and get the reminder r={r}.')
    print(f'{exp} = {x} * {p - 1} + {r}')
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
        if amitte != 0:
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


def multiplicative_inverse_modulo(a, m, out=False):
    """
    m = n * a + rest
    n: is calculated
    rest: is calculated
    :param a:
    :param m:
    :param out:
    :return:
    """
    # modulare multiplikative inverse
    _a = a
    _m = m
    r = 1
    equations = []
    if not out:
        block_print()
    if greatest_common_divisor(a, m, out=False) == 1:
        while r != 0:
            p = m // a
            r = m - (a * p)
            print(f'{m} = {a} * {p} + {r}')
            equations.append((m, a, p, r))
            m = a
            a = r
        print(f'Looking for inverse')
        res = mod_inv(_a, _m)
        print(f'Inverse for a={_a} and m={_m} is: {res}')
        if not out:
            enable_print()
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


def elliptic_curve(P, Q, a, p):
    # y² = x³ + a * x + b mod p
    # calculate s
    s = 0
    (x_1, y_1) = (P[0], P[1])
    (x_2, y_2) = (Q[0], Q[1])
    # print(P, Q)
    if P != Q:
        p1 = (y_2 - y_1)
        p2 = multiplicative_inverse_modulo((x_2 - x_1), p, out=True)
        s = (p1 * p2) % p
        print('Unequal, Punktaddition')
        print(f's = ((y2 - y1) * (x2 - x1)⁻¹) mod p')
        print(f's = ({y_2} - {y_1} * ({x_2} - {x_1})⁻¹) mod {p} = {s}')
    else:
        p1 = (3 * pow(x_1, 2) + a)
        p2 = multiplicative_inverse_modulo((2 * y_1), p, out=True)
        s = (p1 * p2) % p
        print('Equal, Verdopplung')
        print(f's = ((3 * x1² + a) * (2 * y1)⁻¹) mod p')
        print(f's = (3 * {x_1}² + {a} * (2*{y_1})⁻¹) mod {p} = {s}')
    x_3 = (pow(s, 2) - x_1 - x_2)
    x_3 = x_3 % p
    y_3 = (s * (x_1 - x_3) - y_1)
    y_3 = y_3 % p
    print(f'x3 = (s² - x1 - x2) mod p = ({pow(s, 2)} - {x_1} - {x_2}) mod {p} = {x_3}')
    print(f'y3 = (s (x1 - x3) - y1) mod p = ({s} ({x_1} - {x_3}) - {y_1}) mod {p} = {y_3}')

    return x_3, y_3


def diffie_hellman(p, alpha, alice=0, bob=0):
    """
    :param p: modulo num
    :param alpha:
    :param alice: alices private key
    :param bob: bobs private key
    :return:
    """
    if diffie_hellman_check(p, alpha):
        print(f'[Public]Selected Domain Parameter: p = {p}, alpha = {alpha}')

    if not alice:
        a = random.randint(2, (p - 2))
    else:
        a = alice
    print(f'[Alice (private)] a = k_pr,A = {a}')
    if not bob:
        b = random.randint(2, (p - 2))
    else:
        b = bob
    print(f'[Bob (private)] b = k_pr,B = {b}')

    A = pow(alpha, a) % p
    B = pow(alpha, b) % p
    print(f'A = k_pub,A = alpha^a mod p = {alpha}^{a} mod {p} = {A}')
    print(f'B = k_pub,B = alpha^b mod p = {alpha}^{b} mod {p} = {B}')
    print(f'Alice --- {A} ----> Bob')
    print(f'Alice <---- {B} --- Bob')

    print(f'k_AB = B^a mod p = {pow(B, a) % p}')
    print(f'k_BA = A^b mod p = {pow(A, b) % p}')


def diffie_hellman_EC(p, P, alice, bob, a):
    """
    :param p: modulo param, prime number
    :param P: Point (x1, y1)
    :param alice: How often will Alice Calculate the Curve (private Key Alice)
    :param bob: How often will Bob Calculate the Curve (private Key Bob)
    :param a: factor from y² = x³ + a * x + b mod p
    :return:
    """
    print(f'Agree on public parameters:\n prime number p = {p} and point P = {P} on an elliptic curve.')
    P_Base = P
    print('------------------------------------')
    print(f'Alice chooses random Number a = {alice}')
    print(f'Calculate A = k_pubA {alice}{P}')
    if alice == 1:
        P_New = P
    else:
        for i in range(alice - 1):
            P_New = elliptic_curve((P_New if 'P_New' in locals() else P_Base), P, a, p)
            if not i:
                print(f'{i + 2}P = {P} + {P}')
            else:
                print(f'{i + 2}P = {P_New} + {P}')
    k_pub_alice = P_New

    # reset
    del P_New
    print('------------------------------------')
    print(f'Bob chooses random Number b = {bob}')
    print(f'Calculate B = k_pubB {bob}{P}')
    if bob == 1:
        P_New = P
    else:
        for i in range((bob - 1) if bob > 1 else 1):
            P_New = elliptic_curve((P_New if 'P_New' in locals() else P_Base), P, a, p)
            if not i:
                print(f'{i + 2}P = {P} + {P}')
            else:
                print(f'{i + 2}P = {P_New} + {P}')
    k_pub_bob = P_New
    print(f'\nPublic Keys:\n----------- \nAlice: A = {k_pub_alice} \nBob: B = {k_pub_bob}\n-----------')
    print('Take the Public Key, Calc Private Key')

    # reset
    # Tab = alice*B
    del P_New

    P_Base = (k_pub_bob if alice < bob else k_pub_alice)
    tmp = (alice if alice < bob else bob)
    if tmp == 1:
        P_New = P_Base
    else:
        for i in range((tmp - 1) if tmp > 1 else 1):
            P_New = elliptic_curve((P_New if 'P_New' in locals() else P_Base), P_Base, a, p)

    k_priv_alice_bob = P_New

    print(f'b * KpubA = a * KpubB = {bob} * {k_pub_alice} = {alice} * {k_pub_bob}')
    print(f'Private Key for Alice AND Bob: {k_priv_alice_bob}')


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
    d = multiplicative_inverse_modulo(e, phi, out=True)
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
    """
    :param num: Message
    :param p: p
    :param q: q
    :param e: e
    :return:
    """
    # block_print()
    start = time.time_ns()
    if e != 0:
        (n, e), private = RSA(p, q, e)
    else:
        (n, e), private = RSA(p, q)
    if num >= n:
        # enable_print()
        print(f'given number too big. Must be smaller than {n}')
        return
    chiffre = pow(num, e) % n
    cleartext = pow(chiffre, private) % n
    end = time.time_ns()
    # enable_print()
    print(f'Message: {num}')
    print(f'Encrypted: {num}exp({e}) mod {n} = {chiffre}')
    print(f'Decrypted: {chiffre}exp({private}) mod {n} = {cleartext}')
    print(f'Signatur: {num}exp({private}) mod {n} = {pow(num, private) % n}')
    print(f'Verify Signatur: {pow(num, private) % n}exp({e}) mod {n} = {pow(pow(num, private) % n, e) % n}')
    print(f'Total time: {round(round(end - start) / 1000000, 2)} ms')


def hex_to_bin(hexStr):
    return "{0:08b}".format(int(hexStr, 16))


if __name__ == '__main__':
    #### RSA ####
    # message_RSA(4, 13, 7)
    # RSA(5, 11, 7)

    #### Elliptische Kurve ####
    # diffie_hellman_EC(11, (2, 1), 2, 1, 1)

    #### MISC ####
    # print(greatest_common_divisor(2689, 4001))
    # multiplicative_inverse_modulo(2, 11)
    # fermats_little_theorem(7, 26, 53)
    print('Done...')
