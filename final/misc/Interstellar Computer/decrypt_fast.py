import numpy as np

with open('enc.txt', 'r') as file:
    enc = file.readline().encode()

bound1 = 9412912491725612794691274691726592174124019257091257012974019251209481092750129740192750192570500520
bound2 = 1249800259102590129502856015820701258027175017401284082105802184082105702219409520157210580128506126

def mat_pow(mat, p, mod):
    base = np.copy(mat)
    ret = np.eye(mat.shape[0], dtype=object)
    while p > 0:
        if p % 2 == 1:
            ret = np.dot(ret, base) % mod
        base = np.dot(base, base) % mod
        p //= 2
        print(p)
    return ret

def eq_eval_fast(n):
    # equation
    # > 69x^125 + 24x^123 + 19x^98 + 420x^69 + 33x^14 + 2024x + 2025

    # highest rank
    N = 125

    # base matrix
    a = np.ones((N + 2, 1), dtype=object)
    a[0, 0] = 0

    # transform matrix
    b = np.zeros((N + 2, N + 2), dtype=object)
    b[0, 0] = 1

    b[0, 1] = 2025
    b[0, 2] = 2024
    b[0, 15] = 33
    b[0, 70] = 420
    b[0, 99] = 19
    b[0, 124] = 24
    b[0, 126] = 69

    for i in range(1, N + 2):
        b[i, 1] = 1
        for j in range(2, i + 1):
            b[i, j] = b[i - 1, j - 1] + b[i - 1, j]
            
    # calculate
    bn = mat_pow(b, n, bound1 * bound2)
    ret = np.dot(bn, a) % (bound1 * bound2)

    return ret[0, 0]

eval_pad = str(eq_eval_fast(12412847021597012957) * pow(10, 220))

key = bytearray([int(eval_pad[i:(i + 4)]) & 0x7F for i in range(0, 220, 4)])

flag = ''.join([chr(enc[0:55][i] ^ key[i]) for i in range(0, len(key))])

with open('flag.txt', 'w') as file:
    print(flag)
    file.write(flag)
