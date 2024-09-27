import numpy as np

with open('flag.txt', 'r') as file:
    flag = file.readline().encode()

bound1 = 9412912491725612794691274691726592174124019257091257012974019251209481092750129740192750192570500520
bound2 = 1249800259102590129502856015820701258027175017401284082105802184082105702219409520157210580128506126

def eq(x):
    return 69*x**125 + 24*x**123 + 19*x**98 + 420*x**69 + 33*x**14 + 2024*x + 2025

def eq_eval(n):
    ret = 0
    for x in range(1, n + 1):
        ret += eq(x)
    return ret % (bound1 * bound2)

eval_pad = str(eq_eval(12412847021597012957) * pow(10, 220))

key = bytearray([int(eval_pad[i:(i + 4)]) & 0x7F for i in range(0, 220, 4)])

enc = ''.join([chr(flag[0:55][i] ^ key[i]) for i in range(0, len(key))])

with open('enc.txt', 'w') as file:
    print(enc)
    file.write(enc)
