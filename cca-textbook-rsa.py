#!/usr/bin/env python2.7
# coding: utf-8

from Crypto.PublicKey import RSA
import gmpy
import requests

ciphertext = "912fcd40a901aa4b7b60ec37ce6231bb87783b0bf36f824e51fe77e9580ce1adb\
5cf894410ff87684969795525a63e069ee962182f3ff876904193e5eb2f34b20cfa37ec7ae0e939\
1bec3e5aa657246bd80276c373798885e5a986649d27b9e04f1adf8e6218f3c805c341cb38092ab\
771677221f40b72b19c75ad312b6b95eafe2b2a30efe49eb0a5b19a75d0b31849535b717c41748a\
6edd921142cfa7efe692c9a776bb4ece811afbd5a1bbd82251b76e76088d91ed78bf328c6b608bb\
fd8cf1bdf388d4dfa4d4e034a54677a16e16521f7d0213a3500e91d6ad4ac294c7a01995e1128a5\
ac68bfc26304e13c60a6622c1bb6b54b57c8dcfa7651b81576fc"

url = "https://id0-rsa.pub/problem/rsa_oracle/"

pub = RSA.importKey(open('./pubkey.pem','r'))
print '[+] Using key:\n{0}'.format(pub.exportKey())

coprime = 0
r = 2
while not coprime:
    if gmpy.gcd(r,pub.n) == 1:
        coprime = r
    r += 1

chosencipher = format(int(ciphertext, 16) * pow(coprime,pub.e) % pub.n, 'x')
resp = requests.get(url + chosencipher + '/').text.encode('utf-8')
pt = format(int(gmpy.invert(coprime,pub.n)) * int(resp, 16) % pub.n, 'x')

print '\n[+] Plaintext: {0}'.format(pt)
