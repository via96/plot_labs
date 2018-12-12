import time

class Timer:

    def start(self):
        self.start = time.time()
        self.isActive = True

    
    def stop(self):
        if self.isActive:
            self.isActive = False
            return time.time() - self.start
        else:
            return 0