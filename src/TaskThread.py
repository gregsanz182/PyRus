import threading
import time

class TaskThread(threading.Thread):

    def __init__(self, threadNumber):
        super().__init__()
        self.threadNumber = threadNumber

    def run(self):
        begin_time = time.time()
        current_time=0
        while current_time < 5:
            current_time = int(time.time()-begin_time)
            print("Thread {0}: Elapsed Time:{1}".format(self.threadNumber, current_time))
            time.sleep(1)
