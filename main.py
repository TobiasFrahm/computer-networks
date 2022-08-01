#! /bin/python3

import misc
import ellipticCurves
import rsa


if __name__ == '__main__':
    test = misc.Misc()
    testElliptic = ellipticCurves.EllipticCurve()
    testRSA = rsa.RSA()

    #### RSA ####
    #testRSA.message_RSA(8, 5, 11, 7)
    #testRSA.RSA(5, 11, 7)

    #### Elliptische Kurve ####
    #testElliptic.diffie_hellman_EC(7, (2, 5), 2, 1, -43)
    #testElliptic.elliptic_curve((2, 5), (3, 6), -43, 7)

    #### MISC ####

    #test.greatest_common_divisor(40, 7, out=True)
    #test.multiplicative_inverse_modulo(2, 11, out=True)
    #test.fermats_little_theorem(21, 12, 13)
    #test.eulersche_phi(9)
    print('Done...')
