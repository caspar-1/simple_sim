import time
import multiprocessing as mp
#from  simplesimulator.blocks.gui_blocks import GUI_BLOCK
import logging
logger=logging.getLogger(__name__)


class GUI:
    def __init__(self,cntrls):
        self.close_requested=False
        self.process=None
        self.ctx = mp.get_context('spawn')
        self.que=self.ctx.Queue()
        
        self.__cntrls=[]
        for c in cntrls:
            gui_obj=c.get_gui_obj(self.ctx.Value('d',0.0)) 
            self.__cntrls.append(gui_obj)
        pass

    def stop(self):
        self.process.terminate()

    def start(self,target_funct,):
        self.process=self.ctx.Process(target=target_funct,args=(self.que,self.__cntrls,))
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
