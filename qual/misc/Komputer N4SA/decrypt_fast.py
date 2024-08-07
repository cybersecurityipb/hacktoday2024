import numpy as np

with open('enc.txt', 'r') as file:
    enc = file.readline().encode()

bound1 = 1295911241295070912759062510927419182371092570912740917209471290749986192846891264891628946189264982
bound2 = 9124789812750912709571902562640812649812640812640126508126408612084612856193641021290712049605126091
bound3 = 5275097124129650129640129471209719207491206751249012709217590109128390127490172599471092650192750500

def mat_pow(mat, p, mod):
    base = np.copy(mat)
    ret = np.eye(mat.shape[0], dtype=object)
    while p > 0:
        if p % 2 == 1:
            ret = np.dot(ret, base) % mod
        base = np.dot(base, base) % mod
        p //= 2
    return ret

def eq1_eval_fast(n):
    # x + 2

    a = np.array([
        [0],
        [1],
        [1]
    ], dtype=object)
    b = np.array([
        [1, 2, 1],
        [0, 1, 0],
        [0, 1, 1]
    ], dtype=object)
    bn = mat_pow(b, n, (bound1 * bound2))
    ret = np.dot(bn, a) % (bound1 * bound2)
    return ret[0, 0]
def eq2_eval_fast(n):
    # 3x^2 + x + 5

    a = np.array([
        [0],
        [1],
        [1],
        [1]
    ], dtype=object)
    b = np.array([
        [1, 5, 1, 3],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 2, 1]
    ], dtype=object)
    bn = mat_pow(b, n, (bound1 * bound3))
    ret = np.dot(bn, a) % (bound1 * bound3)
    return ret[0, 0]
def eq3_eval_fast(n):
    # 69x^4 + 420(x + 69)^2 + 420x
    # 69x^4 + 420x^2 + 58380x + 1999620

    a = np.array([
        [0],
        [1],
        [1],
        [1],
        [1],
        [1]
    ], dtype=object)
    b = np.array([
        [1, 1999620, 58380, 420, 0, 69],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0],
        [0, 1, 2, 1, 0, 0],
        [0, 1, 3, 3, 1, 0],
        [0, 1, 4, 6, 4, 1]
    ], dtype=object)
    bn = mat_pow(b, n, (bound2 * bound3))
    ret = np.dot(bn, a) % (bound2 * bound3)
    return ret[0, 0]

eval_pad1 = str(eq1_eval_fast(91826498126598612984698126498162984698215011028470182748192650182640812648) * pow(10, 40))
eval_pad2 = str(eq2_eval_fast(61984698126481720571290471920740912759102874091264012640861208461826012842) * pow(10, 80))
eval_pad3 = str(eq3_eval_fast(53289653298649832498103841081365081364802478126583016583160568136501681357) * pow(10, 160))

key1 = bytearray([int(eval_pad1[i:(i + 4)]) & 0x7F for i in range(0, 40, 4)])
key2 = bytearray([int(eval_pad2[i:(i + 4)]) & 0x7F for i in range(0, 80, 4)])
key3 = bytearray([int(eval_pad3[i:(i + 4)]) & 0x7F for i in range(0, 160, 4)])

flag = (
    ''.join([chr(enc[0:10][i] ^ key1[i]) for i in range(0, len(key1))]) +
    ''.join([chr(enc[10:30][i] ^ key2[i]) for i in range(0, len(key2))]) +
    ''.join([chr(enc[30:70][i] ^ key3[i]) for i in range(0, len(key3))])
)

with open('flag.txt', 'w') as file:
    print(flag)
    file.write(flag)

