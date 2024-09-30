import jwt
import json
import random

common_password = "qwerty", "123456", "asdfgh", "zxcvbn"

def weak_password(pwd: str):
    if len(set(pwd.lower())) == 1:
        return True
    if pwd in common_password:
        return True
    if len(pwd) < 13:
        for x in common_password:
            if pwd.startswith(x):
                return True
    return False

with open("jwks.json") as f:
    WHITELISTED = json.loads(f.read()).get("keys")
    f.close()

class Auth:
    def __init__(self, token=""):
        global jwt, WHITELISTED
        self.whitelisted = WHITELISTED
        self.token = None
        self.signkey = None
        self.data = None
        if token:
            self.token = token
            self.load_key()

    def load_key(self):
        global jwt
        if self.token:
            try:
                header = jwt.get_unverified_header(self.token)
                jwks = jwt.PyJWKClient(header.get("jku"))
                jwk = jwks.get_signing_key_from_jwt(self.token)
                for w_jwk in self.whitelisted:
                    w_jwk = jwt.PyJWK.from_dict(w_jwk)
                    if (jwk.key_id == w_jwk.key_id) and (jwk.key.public_numbers().n == w_jwk.key.public_numbers().n):
                        self.signkey = jwk
                        return True
            except:
                pass
        return False
    
    def load(self):
        if self.signkey:
            try:
                self.data = jwt.decode(self.token, self.signkey, algorithms=["RS256"])
                return self.data
            except:
                pass
        return False

    def encode(self, data, url):
        global jwt
        url += ".well-known/jwks.json"
        jwk = random.choice(self.whitelisted)
        jwk = jwt.PyJWK.from_dict(jwk)
        headers = dict(kid=jwk.key_id,jku=url)
        with open(f"jwt_keys/{jwk.key_id}") as f:
            key = f.read()
        token = jwt.encode(data, key, "RS256", headers)
        return token

def emoji():
    a = "(๑•̀ᗝ•́)૭", "(•̀ᴗ•́ )و", "ლ(ಠ益ಠლ)", "(╥﹏╥)", "୧(๑•̀ᗝ•́)૭", "(╯'□')╯︵ ┻━┻", "(๑`^´๑)︻デ═一", "ლ(ಥ益ಥლ)", "( ｡ •̀ ᴖ •́ ｡)💢", "ヽ༼ ಠ益ಠ ༽ﾉ", "凸ಠ益ಠ)凸", "Ψ(`_´ # )↝"
    return random.choice(a)
