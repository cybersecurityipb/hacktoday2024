def xor(data, key):
    return bytes([a ^ b for a, b in zip(data, key)])

bound1 = 1295911241295070912759062510927419182371092570912740917209471290749986192846891264891628946189264982
bound2 = 9124789812750912709571902562640812649812640812640126508126408612084612856193641021290712049605126091
bound3 = 5275097124129650129640129471209719207491206751249012709217590109128390127490172599471092650192750500

def eq1(x):
    return x + 2
def eq2(x):
    return 3 * x**2 + x + 5
def eq3(x):
    return 69 * x**4 + 420 * (x + 69)**2 + 420 * x

#print(eq1(1),eq1(2),eq1(3),eq1(4))
#print(eq2(1),eq2(2),eq2(3),eq2(4))
#print(eq3(1),eq3(2),eq3(3),eq3(4))

def sv1(n,b,a):
	return n // 2*(2*a+(n-1)*b)%(bound1 * bound2)

def sv2(n):
	return  (n**3+2*(n**2)+6*n) % (bound1 * bound3)


large_x = 53289653298649832498103841081365081364802478126583016583160568136501681357
bound2 = 9124789812750912709571902562640812649812640812640126508126408612084612856193641021290712049605126091
bound3 = 5275097124129650129640129471209719207491206751249012709217590109128390127490172599471092650192750500


def a(n, b2, b3):
    sum_x4 = (n * (n + 1) * (2 * n + 1) * (3 * n**2 + 3 * n - 1)) // 30
    return (69 * sum_x4) % (b2 * b3)
def b(n, b2, b3):

    sum_k2 = (n * (n + 1) * (2 * n + 1)) // 6

    sum_k = (n * (n + 1)) // 2

    sum_constant = 4761 * n
    
    total_sum = 420 * (sum_k2 + 138 * sum_k + sum_constant)
    return total_sum % (b2 * b3)

def c(n, b2, b3):
    # Sum of k from 1 to n
    sum_k = (n * (n + 1)) // 2
    
    total_sum = 420 * sum_k
    return total_sum % (b2 * b3)

sumofall = ((a(large_x, bound2, bound3) % (bound2 * bound3)) + (b(large_x, bound2, bound3) % (bound2 * bound3)) + (c(large_x, bound2, bound3) % (bound2 * bound3))) % (bound2 * bound3)

eval_pad1 = str(sv1(91826498126598612984698126498162984698215011028470182748192650182640812648,1,3) * pow(10, 40))
eval_pad2 = str(sv2(61984698126481720571290471920740912759102874091264012640861208461826012842)* pow(10, 80))
eval_pad3 = str(sumofall*pow(10,160))
key1 = bytearray([int(eval_pad1[i:(i + 4)]) & 0x7F for i in range(0, 40, 4)])
key2 = bytearray([int(eval_pad2[i:(i + 4)]) & 0x7F for i in range(0, 80, 4)])
key3 = bytearray([int(eval_pad3[i:(i + 4)]) & 0x7F for i in range(0, 160, 4)])

flag = open('enc.txt','rb').read()

enc = (
    ''.join([chr(flag[0:10][i] ^ key1[i]) for i in range(0, len(key1))]) +
    ''.join([chr(flag[10:30][i] ^ key2[i]) for i in range(0, len(key2))]) +
    ''.join([chr(flag[30:70][i] ^ key3[i]) for i in range(0, len(key3))])
)
print(enc)
print(xor(flag,key1+key2+key3))
