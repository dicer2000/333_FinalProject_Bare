from threading import Event, Thread, Lock
import copy

# Thread-safe global objects
class SafeFrame(object):
    def __init__(self, startval = None):
        self.lock = Lock()
        self.value = startval
    def set(self, val):
        self.lock.acquire(True, 0.1)
        try:
            self.value = val
        finally:
            self.lock.release()
    def get(self):
        self.lock.acquire()
        try:
            return copy.deepcopy(self.value)
        finally:
            self.lock.release()

class SafeExiting(object):
    def __init__(self, startval = False):
        self.lock = Lock()
        self.value = startval
    def set(self, exiting):
        with self.lock:
            self.value = exiting
    def get(self):
        with self.lock:
            return self.value
