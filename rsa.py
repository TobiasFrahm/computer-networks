import misc
import time


class RSA:
    miscCalculator = 0

    def __init__(self):
        self.miscCalculator = misc.Misc()

    def RSA(self, p, q, e=0):
        """
        :param p: prime number
        :param q: prime number
        :param e: public key
        :return:
        """
        print('Basic principal is a big number, decomposed in its prime factors')
        print('and the decomposition into prime factors')
        print('Key Generation')
        print('Each participant chooses two random prime factors p and q and chooses the numbers e and d as follows:')
        n = p * q
        print(f'n = p * q = {p} * {q} = {n}')
        print(f'phi(n) = phi({n}) = (p - 1) * (q - 1) = {(p - 1) * (q - 1)}')
        phi = self.miscCalculator.eulersche_phi(n)
        if e == 0:
            print(f'Choose a small odd number e between 1 < e < phi(n) and ggT(e, phi(n)) == 1')
            e = 0
            for possible_e in range(2, phi):
                # is possible_e odd?
                if possible_e % 2 != 0:
                    if self.miscCalculator.greatest_common_divisor(possible_e, phi) == 1:
                        e = possible_e
                        print(f'Public Key(calculated): e = {e}')
                        break
        else:
            print(f'Public Key(given): e = {e}')

        print('Private Key d is a number: 1 < d < phi(n) and e*d = 1 mod phi(n)')
        d = self.miscCalculator.multiplicative_inverse_modulo(e, phi, out=True)
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

    def message_RSA(self, num, p, q, e=0):
        """
        :param num: Message
        :param p: p
        :param q: q
        :param e: e
        :return:
        """
        start = time.time_ns()
        if e != 0:
            (n, e), private = self.RSA(p, q, e)
        else:
            (n, e), private = self.RSA(p, q)
        if num >= n:
            print(f'given number too big. Must be smaller than {n}')
            return
        # FYI: private = d
        chiffre = pow(num, e) % n
        cleartext = pow(chiffre, private) % n
        end = time.time_ns()
        print(f'Message: {num}')
        print(f'Encrypted: {num}exp({e}) mod {n} = {chiffre}')
        print(f'Decrypted: {chiffre}exp({private}) mod {n} = {cleartext}')
        print(f'Signatur: {num}exp({private}) mod {n} = {pow(num, private) % n}')
        print(f'Verify Signatur: {pow(num, private) % n}exp({e}) mod {n} = {pow(pow(num, private) % n, e) % n}')
        print(f'Total time: {round(round(end - start) / 1000000, 2)} ms')
