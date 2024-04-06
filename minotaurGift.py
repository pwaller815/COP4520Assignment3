# Parker Waller
# Assignment 3 Part 1
# COP 4520
# 4/4/24

import threading
from threading import Thread
import random

GIFTS = 500000
index = 0
lock = threading.Lock()

class node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.locked = False

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

class linked_list:
    def __init__(self):
        self.head = node("HEAD")
        self.size = 0

    def insert(self, data):
        new_node = node(data)
        # Base case
        if not self.head.next:
            self.head.next = new_node
            self.size +=1
            return True
        # Normal
        pred = self.head
        pred.lock()
        try:
            curr = pred.next
            while curr:
                if curr.locked:  
                    pred.unlock()
                    return False
                curr.lock()
                try:
                    if data > curr.data:
                        if not curr.next:
                            curr.next = new_node
                            self.size += 1
                            return True
                        pred.unlock()
                        pred = curr
                        curr = curr.next
                    else:
                        new_node.next = curr
                        pred.next = new_node
                        self.size += 1
                        return True
                finally:
                    curr.unlock()
        finally:
            pred.unlock()

    def contains(self, data):
        curr = self.head
        while curr.next:
            if data == curr.next.data:
                if curr.next.locked:
                    return 0
                return 1
            curr = curr.next
        return -1

    def remove(self):
        if self.size == 0:
            return 0
        if not self.head.next or self.head.locked:
            return -1
        self.head.lock()
        if self.head.next and self.head.next.locked:
            return -1
        else:
            if self.head.next and self.head.next.next:
                self.head.next.lock()
                self.head.next = self.head.next.next
            else:
                self.head.next = None
        self.head.unlock()
        self.size -= 1
        return 1
        
def servant(ll, bag, thread_id):
    global index
    while index < GIFTS or ll.size != 0:
        work = random.randint(1,3)
        if work == 1:
            thr_index = -1
            with lock:
                thr_index = index
                index += 1
            if thr_index >= GIFTS:
                return
            while not ll.insert(bag[thr_index]):
                pass
        if work == 2:
            search = random.randint(1, GIFTS)
            while ll.contains(search) == 0:
                ll.contains(search)
        else:
            result = ll.remove()
            while result == -1:
                result = ll.remove()
                    
def main():
    ll = linked_list()
    # Create array of gifts and randomize them
    bag = [i for i in range(1, GIFTS+1)]
    random.shuffle(bag)
    # Intialize and start threads
    threads = []
    for i in range(4):
        thr = Thread(target=servant,args=(ll,bag,i+1,))
        thr.start()
        threads.append(thr)

    for thr in threads:
        thr.join()

    print("All letter sent.")

main()
