from Crypto.Util.number import *
from fastecdsa.curve import Curve
import hashlib, json

class ECDSA:
    def __init__(self, privKey):
        self.Curve = Curve(
            'secp256k1',
            0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f,
            0x0000000000000000000000000000000000000000000000000000000000000000,
            0x0000000000000000000000000000000000000000000000000000000000000007,
            0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141,
            0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
            0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
        )
        self.privKey = privKey
        self.pubKey = self.Curve.G * self.privKey

    def get_nonce(self):
        _A = 2**128 - 1
        randomNum = getRandomNBitInteger(128)
        moreRandomNum = (randomNum + _A) - 2 * (randomNum & _A)
        final_nonce = int.from_bytes(randomNum.to_bytes(16, 'big') + moreRandomNum.to_bytes(16, 'big'), 'big')
        return final_nonce

    def hash_msg(self, msg):
        return int(hashlib.sha256(msg).hexdigest(), 16)

    def sign(self, msg):
        k = self.get_nonce()
        z = self.hash_msg(msg)
        r = (self.Curve.G * k).x    
        s = pow(k, -1, self.Curve.q) * (z + r * self.privKey) % self.Curve.q
        return json.dumps({'r' : hex(r), 's' : hex(s), 'msg' : msg.hex()})

    def verify(self, signature):
        r = int(signature['r'], 16)
        s = int(signature['s'], 16)
        msg = bytes.fromhex(signature['msg'])
        if (not (1 <= r <= (self.Curve.q - 1))) or (not (1 <= s <= (self.Curve.q - 1))):
            return False
        z = self.hash_msg(msg)
        u1 = z * pow(s, -1, self.Curve.q) % self.Curve.q
        u2 = r * pow(s, -1, self.Curve.q) % self.Curve.q
        return r == (self.Curve.G * u1 + self.pubKey * u2).x