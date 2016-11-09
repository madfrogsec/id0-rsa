#!/usr/bin/env python2.7
# coding: utf-8

import Queue
import threading
import os
import time
import hashlib
import base64

time_start = time.time()
index = 0

threads = 4
queue = Queue.Queue()

min_value = int(hashlib.sha256('toto').hexdigest(), 16)
max_value = 0
(min_word, max_word) = ('','')


hashes = ['$(y3]<+9zmi4|$6Rup8P8oJnxK98aXa8HhGROLdvws9xmgawl7rsh2E5E=',
'$b*.m,%~&<"^6$l93FR8Rq8a+YIUdcC2Kdake7/rlSU1zAr/9yAiRZVI0=',
'$9bOv^Gu)oB&P$EdEfD9X20gQi+sUYRvHyuoCMGq7DCeD/UJSSDmCvjZA=',
'$kPD)T)=~1K{r$BgOuh0tBaGKtcFscQvdwFBscgC+pYKW1qpFDDwTJRAA=',
'$4.9.mHSbiQ]^$by2hg2rG18QKk9pMqa/Fb9vnJ5/NEvR5qpg9SVdy3nM=',
'${4[1m"WqdR0s$Vz+gAWYf/8PIKu7ILxaVFnDcNCzAcerci8caiCYgm2Y=',
'$3ui!yKfT0[Si$QZJcfHWh+OsdkgkrrZNp8ZkYlc3sWlT57PgC/YhmaRY=']

test_hashes = ["$F&XUtH6krgmy$jZ83Epqxk7QUo7D6Rev2AEfQuvMHokwm/QBQDfR+r6Q=",
"$UA~R<9E'\n9\$6XP2CXRjVfmCcuz2OWCtLPIVI/1J9ZQojr+MxRCUY/E=",
"$_)lOt8&:j5%f$Gu99fWD+K8lsHE+0lizszH8Kkb5QPrjz3osT4/LFexo="]

b64decoded_hashes = []
cracked = []

def showElapsedTime():
    elapsed_time = time.time() - time_start
    print '[+] {0} words tested in {1:.2f}s'.format(index, float(elapsed_time))

def showSpeed():
    elapsed_time = time.time() - time_start
    print '[+] Speed: {0:.2f} hash/s'.format(index/elapsed_time)

def showCracked():
    global cracked
    if cracked:
        for e in cracked:
            print '[+] Hash : {0}'.format(base64.encodestring(e[0][1].decode('hex')))
            print '[+] Word : {0}'.format(e[1])

class Worker(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue=queue
        self.kill_received = False

    def run(self):
        global cracked, index
        while not self.kill_received:
            self.clear = self.queue.get()

            for e in b64decoded_hashes:
                # print '\n' + hashlib.sha256(self.clear + e[0]).hexdigest()
                # print e[1]
                if hashlib.sha256(self.clear + e[0]).hexdigest() == e[1]:
                    cracked.append([e,self.clear])
            index += 1
            if index % 500000 == 0:
                showSpeed()
                showElapsedTime()
            self.queue.task_done()

def main():
    global b64decoded_hashes
    try:
        for e in hashes:
            tab = e.split('$')
            hexhash = base64.decodestring(tab[2]).encode('hex')
            b64decoded_hashes.append([tab[1], hexhash])

        for i in xrange(threads):
            t = Worker(queue)
            t.daemon = True
            t.start()

        with open('./rockyou.txt','rb') as wl:
            for word in wl.readlines():
                queue.put(word.strip())
        queue.join()

        showSpeed()
        showElapsedTime()
        showCracked()
        os._exit(0)

    except KeyboardInterrupt:
        print '\n[+] Keyboard Interrupt...'
        showElapsedTime()
        showCracked()
        os._exit(1)

if __name__ == '__main__':
    main()
