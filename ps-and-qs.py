#!/usr/bin/env python2.7
# coding: utf-8

from Crypto.PublicKey import RSA
import gmpy

message = "0f5ed9da29d8d260f22657e091f34eb930bc42f26f1e023f863ba13bee39071d1ea9\
88ca62b9ad59d4f234fa7d682e22ce3194bbe5b801df3bd976db06b944da"
raw_message = message.decode('hex')

pubkey = RSA.importKey(open('./pubkey.pem').read())
pubkey_alt = RSA.importKey(open('pubkey-alt.pem').read())

pgcd = gmpy.gcd(pubkey.n, pubkey_alt.n)

print '[+] PGCD(n, n-alt): {0}'.format(pgcd)
print '[+] N             : {0}'.format(pubkey.n)
print '[+] P/N           : {0}'.format(pubkey.n / pgcd)

p = long(pgcd)
q = long(pubkey.n / pgcd)
d = long(gmpy.invert(pubkey.e,(p-1)*(q-1)))

privkey = RSA.construct((pubkey.n, pubkey.e, d, p, q))

print '\n[+] Private Key: \n{0}'.format(privkey.exportKey())
print '\n[+] Message    : {0}'.format(privkey.decrypt(raw_message).encode('hex'))

# f6a1df363229c6ec
