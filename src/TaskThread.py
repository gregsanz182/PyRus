import threading
import time
from EncoderTools import EncoderTools

class TaskThread(threading.Thread):

    def __init__(self, threadNumber, audioFile, tool):
        super().__init__()
        self.threadNumber = threadNumber
        self.audioFile = audioFile
        self.tool = tool

    def run(self):
        begin_time = time.time()
        current_time=0
        self.tool.prepareCMDLine(self.audioFile)
