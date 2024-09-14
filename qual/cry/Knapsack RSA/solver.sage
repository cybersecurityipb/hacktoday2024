from itertools import combinations
from tqdm import tqdm
from hashlib import sha256
from Crypto.Util.number import *
from Crypto.Cipher import AES
from itertools import combinations

def generate_subset_sums(arr):
    subset_sums = {}
    n = len(arr)
    for r in tqdm(range(n + 1)):
        for subset in combinations(range(n), r):
            subset_sum = sum(arr[i] for i in subset)
            subset_sums[subset_sum] = subset
    return subset_sums

def subset_sum_meet_in_middle(arr, target):
    n = len(arr)
    left_half = arr[:n//2]
    right_half = arr[n//2:]
    
    left_sums = generate_subset_sums(left_half)
    right_sums = generate_subset_sums(right_half)
    
    if target in left_sums:
        return left_sums[target]
    if target in right_sums:
        return tuple(i + n//2 for i in right_sums[target])
    
    right_sums_keys = sorted(right_sums.keys())
    
    for left_sum, left_indices in tqdm(left_sums.items()):
        required_sum = target - left_sum
        low, high = 0, len(right_sums_keys) - 1
        while low <= high:
            mid = (low + high) // 2
            if right_sums_keys[mid] == required_sum:
                right_indices = right_sums[required_sum]
                return left_indices + tuple(i + n//2 for i in right_indices)
            elif right_sums_keys[mid] < required_sum:
                low = mid + 1
            else:
                high = mid - 1

    return None

def decrypt(ct,key):
    cipher = AES.new(key, AES.MODE_CBC, ct[:16])
    res = cipher.decrypt(ct[16:])
    return res


mult = []
for arr, weightt in zip(out,weight):
    res = subset_sum_meet_in_middle(arr, weightt)
    mult.append([arr[i] if i in res else 0 for i in range(len(arr))])
    assert(sum(mult[-1]) == weightt)

flag1 = "".join('0' if j == 0 else '1' for i in mult for j in i)
flag1 = long_to_bytes(int(flag1,2))
print(flag1)

keys = 0
e = 11

for i in tqdm(range(len(mult[0]))):
    temp = [mult[0][i], mult[1][i], mult[2][i], mult[3][i]]
    summ = temp.count(0)
    if summ == 4:
        continue
    elif summ == 3:
        keys ^^= sums[i]
    elif summ == 2:
        temp = [m for m in temp if m != 0]
        PR.<x1, x2> = PolynomialRing(Zmod(n))
        eqs = [x1+x2-sums[i], x1**e-temp[0],x2**e-temp[1]]
        for eq in Ideal(eqs).groebner_basis():
            keys ^^= int((-eq%n).coefficients()[-1])
    elif summ == 1:
        temp = [m for m in temp if m != 0]
        PR.<x1, x2, x3> = PolynomialRing(Zmod(n))
        eqs = [x1+x2+x3-sums[i], x1**e-temp[0],x2**e-temp[1],x3**e-temp[2]]
        for eq in Ideal(eqs).groebner_basis():
            keys ^^= int((-eq%n).coefficients()[-1])
    elif summ == 0:
        temp = [m for m in temp if m != 0]
        PR.<x1, x2, x3, x4> = PolynomialRing(Zmod(n))
        eqs = [x1+x2+x3+x4-sums[i], x1**e-temp[0],x2**e-temp[1],x3**e-temp[2],x4**e-temp[3]]
        for eq in Ideal(eqs).groebner_basis():
            keys ^^= int((-eq%n).coefficients()[-1])
    
keys = sha256(long_to_bytes(keys)).digest()
ct = bytes.fromhex(ct)
decrypt(ct,keys)
print((flag1 + flag2).decode())
