import math

file = open('output.txt', 'r')
Lines = file.readlines()
file.close()

x = int((Lines[0].split())[2], 16) 
n = int((Lines[1].split())[2], 16)
c = int((Lines[2].split())[2], 16)

def solve_rsa_primes(s: int, m: int) -> tuple:
    '''
    Solve RSA prime numbers (p, q) from the quadratic equation
    p^2 - s * p + m = 0 with the formula p = s/2 +/- sqrt((s/2)^2 - m)

    Input: s - sum of primes, m - product of primes
    Output: (p, q)
    '''
    half_s = s >> 1
    tmp = math.isqrt(half_s ** 2 - m)
    return int(half_s + tmp), int(half_s - tmp);  

# Now run with the real input
p, q = solve_rsa_primes(x, n)
m = math.lcm(p - 1, q - 1)
e = 65537
d = pow(e, -1, m)
FLAG = pow(c, d, n)
print(FLAG.to_bytes((FLAG.bit_length() + 7) // 8, 'big'))
