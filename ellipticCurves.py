import misc
import random

class EllipticCurve:

    def diffie_hellman_EC(self, p, P, alice, bob, a):
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
                P_New = self.elliptic_curve((P_New if 'P_New' in locals() else P_Base), P, a, p)
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
                P_New = self.elliptic_curve((P_New if 'P_New' in locals() else P_Base), P, a, p)
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
                P_New = self.elliptic_curve((P_New if 'P_New' in locals() else P_Base), P_Base, a, p)

        k_priv_alice_bob = P_New

        print(f'b * KpubA = a * KpubB = {bob} * {k_pub_alice} = {alice} * {k_pub_bob}')
        print(f'Private Key for Alice AND Bob: {k_priv_alice_bob}')

    def elliptic_curve(self, P, Q, a, p):
        calculator = misc.Misc()
        # y² = x³ + a * x + b mod p
        # calculate s
        s = 0
        (x_1, y_1) = (P[0], P[1])
        (x_2, y_2) = (Q[0], Q[1])
        # print(P, Q)
        if P != Q:
            p1 = (y_2 - y_1)
            p2 = calculator.multiplicative_inverse_modulo((x_2 - x_1), p, out=True)
            s = (p1 * p2) % p
            print('Unequal, Punktaddition')
            print(f's = ((y2 - y1) * (x2 - x1)⁻¹) mod p')
            print(f's = ({y_2} - {y_1} * ({x_2} - {x_1})⁻¹) mod {p} = {s}')
        else:
            p1 = (3 * pow(x_1, 2) + a)
            p2 = calculator.multiplicative_inverse_modulo((2 * y_1), p, out=True)
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

    def diffie_hellman_check(self, p, a):
        if a > (p - 2):
            print('alpha too big')
            return False

        for x in range(2, p):
            if p % x == 0:
                print(f'p = {p} is not a prime number')
                return False
        return True

    def diffie_hellman(self, p, alpha, alice=0, bob=0):
        """
        :param p: modulo num
        :param alpha:
        :param alice: alices private key
        :param bob: bobs private key
        :return:
        """
        if self.diffie_hellman_check(p, alpha):
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
