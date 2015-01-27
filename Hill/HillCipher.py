from numpy import matrix as _matrix
from numpy import linalg as _linalg
import numpy
class HillCipher(object):
    def __init__(self, key, ikey):
        self.key = key
        self.ikey = ikey

    def encrypt(self, plain_text):
        a = _matrix(plain_text)
        k = _matrix(self.key)
        a_k = a*k
        a_k = a_k.tolist()
        return a_k[0]

    def decrypt(self, cipher_text):
        a = _matrix(cipher_text)
        k = _matrix(self.ikey)
        a_k = a*k
        a_k = a_k.tolist()
        return a_k[0]