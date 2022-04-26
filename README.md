# encryption-decrypted
This tool should help learning and understanding the math and logic behind
RSA, elliptic curve, and modula operation used for cryptography algorithm.
It prints out more or less every calculation step. 
Just uncomment the function you want to use, put your values into it
and run it with a python3+ Interpreter.

Surprisingly there is here and there a clone, if you have any ask questions. Feel free to reach out.

RSA
```py RSA
message_RSA(8, 5, 11, 7)
```
Output:
```py Output
Basic principal is a big number, decomposed in its prime factors
and the decomposition into prime factors
Key Generation
Each participant chooses two random prime factors p and q and chooses the numbers e and d as follows:
n = p * q = 5 * 11 = 55
phi(n) = phi(55) = (p - 1) * (q - 1) = 40
Greatest common divisor: 1
phi(55) = 40
Public Key(given): e = 7
Private Key d is a number: 1 < d < phi(n) and e*d = 1 mod phi(n)
Calculating the greatest common divisor of 7, 40 ...
40 = 5 * 7 + 5
7 = 1 * 5 + 2
5 = 2 * 2 + 1
2 = 2 * 1 + 0
Greatest common divisor: 1
40 = 7 * 5 + 5
7 = 5 * 1 + 2
5 = 2 * 2 + 1
2 = 1 * 2 + 0
Looking for inverse
7 = 1 * 7 + 0 * 40
5 = -5 * 7 + 1 * 40
2 = 6 * 7 + -1 * 40
1 = -17 * 7 + 3 * 40
Inverse for a=7 and m=40 is: 23
d = 23
----------------------------------
Public Key (e, n): (7, 55)
Private Key d: 23
Message: 8
Encrypted: 8exp(7) mod 55 = 2
Decrypted: 2exp(23) mod 55 = 8
Signatur: 8exp(23) mod 55 = 17
Verify Signatur: 17exp(7) mod 55 = 8
Total time: 3.93 ms
Done...
```



