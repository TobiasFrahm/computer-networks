import sys
import os
from color import Color as c
from itertools import chain


class Misc:

    def greatest_common_divisor(self, a, b, out=False):
        # ggT(a, b)
        print(f'Calculating the greatest common divisor of {a}, {b} ...')
        if not out:
            self.disable_print()
        r = 0
        if a == 0:
            return abs(b)
        if b == 0:
            return abs(a)
        while b != 0:
            r = a % b
            a = b
            b = r
            try:
                if a % b != 0:
                    print(f'{a} = {int(a / b)} * {b} + {a % b}')
                else:
                    print(f'{a} = {int(a / b)} *', c.CYAN.value + f'{b}' + c.END.value + f' + {a % b}')
            except BaseException as err:
                pass
        if not out:
            self.enable_print()
        print(f'Greatest common divisor: {abs(a)}')
        return abs(a)

    def multiplicative_inverse_modulo(self, a, m, out=False):
        """
        m = n * a + rest
        n: is calculated
        rest: is calculated
        :param a:
        :param m:
        :param out:
        :return:
        """
        _a = a
        _m = m
        r = 1
        equations = []
        if not out:
            self.disable_print()
        if self.greatest_common_divisor(a, m, out=True) == 1:
            while r != 0:
                p = m // a
                r = m - (a * p)
                print(f'{m} = {a} * {p} + {r}')
                equations.append((m, a, p, r))
                m = a
                a = r
            print(f'Looking for inverse')
            res = self.__mod_inv(_a, _m)
            print(f'Inverse for a={_a} and m={_m} is: {res}')
            if not out:
                self.enable_print()
            return res
        else:
            print('Greatest common divisor is not 1')
            print('exit')
            if not out:
                self.enable_print()
            return 0

    def __mod_inv(self, a, m):
        # source https://www.inf-schule.de/kommunikation/kryptologie/rsa/modmultiplikation/station_berechnungmodinv
        (ggt, x, y) = self.__extended_euclidean_algorithm(a, m)
        if ggt > 1:
            print(f'Inverse does not exists, ggT({a},{m}) > 1')
            return -1
        else:
            if x < 0:
                x = x + m
            return x

    def __extended_euclidean_algorithm(self, a, b):
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

    def fermats_little_theorem(self, a, exp, p):
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

    def eulersche_phi(self, n):
        body = []
        phi = 0
        # print(f'Calculate the Body for n={n}')
        self.disable_print()
        for i in range(n):
            if self.__is_not_comparable(i, n):
                # phi(n) is the number of coprime numbers within the body of n
                # phi(n) = n - 1 if n i a prime number
                # phi(i * n) = phi(i) * phi(n), if ggT(i,n) = 1
                phi += 1
            body.append(i + 1)
        self.enable_print()
        print(f'phi({n}) = {phi}')
        return phi

    def __is_not_comparable(self, a, b, out=False):
        res = False
        if not out:
            self.disable_print()
        print(f'Check if {a}, {b} are coprime to each other...')

        if self.greatest_common_divisor(a, b) == 1:
            print(f'{a}, {b} are coprime to each other')
            res = True
        else:
            print(f'{a}, {b} are NOT coprime to each other')
            res = False

        if not out:
            self.enable_print()
        return res

    def hex_to_bin(self, hexStr):
        return "{0:08b}".format(int(hexStr, 16))

    def faktorisiere(self, n):
        l = []  # Lösungsmenge
        # Auf Teilbarkeit durch 2, und alle ungeraden Zahlen von 3..n/2 testen
        for i in chain([2], range(3, n // 2 + 1, 2)):
            # Ein Teiler kann mehrfach vorkommen (z.B. 4 = 2 * 2), deswegen:
            while n % i == 0:
                l.append(i)
                n = n // i  # "//" ist ganzzahlige Division und entspricht int(n/i)
            if i > n:  # Alle Teiler gefunden? Dann Abbruch.
                break
        return l

    def disable_print(self):
        # Disable
        sys.stdout = open(os.devnull, 'w')

    def enable_print(self):
        # Restore
        sys.stdout = sys.__stdout__
