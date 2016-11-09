#!/usr/bin/env python2.7
# coding: utf-8

import gmpy

charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ,."

cipher = open('./ciphertext', 'r').read()
plain = ""

list_coprime = []
lench = len(charset)

def myord(l):
    return charset.index(l)

def mychr(n):
    return charset[n]

def getCoprime(n):
    global list_coprime
    list_coprime.append([i for i in range(n) if gmpy.gcd(lench,i) == 1])

def decryptAffineCipher(a,b):
    return ''.join( mychr((a*(myord(e)-b)) % lench ) for e in cipher.strip() )

def encryptAffineCipher(a,b,plaintext):
    return ''.join( mychr((a*myord(e)+b) % lench ) for e in plain )


def main():

    getCoprime(lench)
    for a in list_coprime[0]:
        for index in range(lench):
            print "\n[+] Using key: a={0}, b={1}".format(a,index)
            print decryptAffineCipher(gmpy.invert(a,lench),index)


if __name__ == '__main__':
    main()

# [+] Using key: a=18, b=23
# COMMERCE ON THE INTERNET HAS COME TO RELY ALMOST EXCLUSIVELY ON FINANCIAL
# INSTITUTIONS SERVING ASTRUSTED THIRD PARTIES TO PROCESS ELECTRONIC PAYMENTS.
# WHILE THE SYSTEM WORKS WELL ENOUGH FORMOST TRANSACTIONS, IT STILL SUFFERS FROM
# THE INHERENT WEAKNESSES OF THE TRUST BASED MODEL. COMPLETELY NONREVERSIBLE
# TRANSACTIONS ARE NOT REALLY POSSIBLE, SINCE FINANCIAL INSTITUTIONS CANNOTAVOID
# MEDIATING DISPUTES. THE COST OF MEDIATION INCREASES TRANSACTION COSTS,
# LIMITING THEMINIMUM PRACTICAL TRANSACTION SIZE AND CUTTING OFF THE POSSIBILITY
# FOR SMALL CASUAL TRANSACTIONS,AND THERE IS A BROADER COST IN THE LOSS OF
# ABILITY TO MAKE NONREVERSIBLE PAYMENTS FOR NONREVERSIBLESERVICES. WITH THE
# POSSIBILITY OF REVERSAL, THE NEED FOR TRUST SPREADS. MERCHANTS MUSTBE WARY OF
# THEIR CUSTOMERS, HASSLING THEM FOR MORE INFORMATION THAN THEY WOULD OTHERWISE
# NEED. A CERTAIN PERCENTAGE OF FRAUD IS ACCEPTED AS UNAVOIDABLE. THESE COSTS
# AND PAYMENT UNCERTAINTIESCAN BE AVOIDED IN PERSON BY USING PHYSICAL CURRENCY,
# BUT NO MECHANISM EXISTS TO MAKE PAYMENTSOVER A COMMUNICATIONS CHANNEL WITHOUT
# A TRUSTED PARTY.

# hashlib.md5 : 880cabd53df2f03050a7214d3ae30a07
