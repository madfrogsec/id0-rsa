#!/usr/bin/env python2.7
# coding: utf-8

import Queue
import threading
import os
import time
import hashlib

time_start = time.time()
index = 0

threads = 4
queue = Queue.Queue()

min_value = int(hashlib.sha256('toto').hexdigest(), 16)
max_value = 0
(min_word, max_word) = ('','')

def showElapsedTime():
    elapsed_time = time.time() - time_start
    print '[+] {0} words tested in {1:.2f}s'.format(index, float(elapsed_time))

def showSpeed():
    elapsed_time = time.time() - time_start
    print '[+] Speed: {0:.2f} hash/s'.format(index/elapsed_time)

class Worker(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue=queue
        self.kill_received = False

    def run(self):
        global min_value, max_value, index, min_word, max_word
        while not self.kill_received:
            self.clear=self.queue.get()
            hash_value = int(hashlib.sha256(self.clear).hexdigest(), 16)
            if hash_value < min_value:
                min_value = hash_value
                min_word = self.clear
            elif hash_value > max_value:
                max_value = hash_value
                max_word = self.clear
            index += 1
            if index % 100000 == 0:
                showSpeed()
                showElapsedTime()
            self.queue.task_done()

def main():
    try:
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

        print '[+] Smallest hash: {0}'.format(min_value)
        print '[+] Corresponding word: {0}\n'.format(min_word)
        print '[+] Greatest hash: {0}'.format(max_value)
        print '[+] Corresponding word: {0}'.format(max_word)
        os._exit(0)

    except KeyboardInterrupt:
        print '\n[+] Keyboard Interrupt...'
        showElapsedTime()
        os._exit(1)

if __name__ == '__main__':
    main()
