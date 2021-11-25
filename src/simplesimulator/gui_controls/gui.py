import time
from multiprocessing import Process,Queue

import logging
logger=logging.getLogger(__name__)


class GUI:
    def __init__(self,cntrls):
        self.close_requested=False
        self.process=None
        self.que=Queue()
        self.__cntrls=[c.gui_obj for c in cntrls]


    def stop(self):
        self.process.terminate()

    def start(self,target_funct,):
        self.process=Process(target=target_funct,args=(self.que,self.__cntrls,))
        self.process.start()
        logger.debug("Simple Simulator Controls window started")
        self.que.get() 
        logger.debug("Simple Simulator Controls window started running")

    @property
    def is_alive(self):
        if self.process:
            return self.process.is_alive()
        else:
            return False
