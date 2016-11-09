#!/usr/bin/env python2.7
# coding: utf-8

import gnupg
import Queue
import threading
import os
import time

time_start = time.time()
index = 0

threads = 4
queue = Queue.Queue()
gpg = gnupg.GPG()

with open('./hello-pgp.cipher','rb') as f:
    cipher = f.read()
wl = open('../wordlists/corncob_lowercase.txt','r')

def showElapsedTime():
    elapsed_time = time.time() - time_start
    print '[+] {0} words tested in {1:.2f}s'.format(index, float(elapsed_time))

def showSpeed():
    elapsed_time = time.time() - time_start
    print '[+] Speed: {0:.2f} words/s'.format(index/elapsed_time)

class Worker(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue=queue
        self.kill_received = False

    def run(self):
        global index
        while not self.kill_received:
            self.clear=self.queue.get()
            data = gpg.decrypt(cipher, passphrase=self.clear.strip())
            if data.data != '':
                print '\n[+] Password found: {}'.format(self.clear)
                print '[+] Decrypted data: {}'.format(data.data)
                showElapsedTime()
                os._exit(0)
            index += 1
            if index % 1000 == 0:
                showElapsedTime()
                showSpeed()
            self.queue.task_done()

def main():
    try:
        for i in xrange(threads):
            t = Worker(queue)
            t.daemon = True
            t.start()

        for word in wl.readlines():
            queue.put(word.strip())
        queue.join()

        print '\n[+] Password not found'
        showElapsedTime()
        os._exit(1)

    except KeyboardInterrupt:
        print '\n[+] Keyboard Interrupt...'
        showElapsedTime()
        os._exit(1)

if __name__ == '__main__':
    main()

# [+] Password found: seamanship
# [+] Decrypted data: passionately apathetic
# [+] 45001 words tested in 142.02s
