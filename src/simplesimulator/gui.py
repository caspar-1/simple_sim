from tkinter import *
import time
from multiprocessing import Process

import logging
logger=logging.getLogger(__name__)


class GUI:
    def __init__(self,cntrls):
        self.close_requested=False
        self.root=None
        self.cntrls=cntrls
        self.process=None

    def __close_window(self):
        self.close_requested=True

    def stop(self):
        self.process.terminate()


    def periodic_call(self):
        if not self.close_requested:
            self.root.after(500, self.periodic_call)
        else:
            logger.debug("Destroying GUI at:", time.time())
            try: 
                self.root.quit()
                
            except:
                pass

    def tkinter_loop(self):
        self.is_running=True
        self.root=Tk()
        self.root.title("Simple Simulator Controls")
        self.root.protocol("WM_DELETE_WINDOW", self.__close_window)
        for c in self.cntrls:
            c.add_cntrl(self.root)

        self.root.after_idle(self.periodic_call)
        self.root.mainloop()
        self.is_running=False
       
        logger.debug("Simple Simulator Controls window finished")

    def start(self):
        self.process=Process(target=self.tkinter_loop)
        self.process.start()
        logger.debug("Simple Simulator Controls window started")

    @property
    def is_alive(self):
        if self.process:
            return self.process.is_alive()
        else:
            return False

if __name__=="__main__":
    from simplesimulator import runtime,blocks
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S')
    logger=logging.getLogger(__name__)




    radio=blocks.gui_controls.RadioGroup()
    radio.add("A")
    radio.add("B")
    radio.add("C")
    s1=blocks.gui_controls.Slider(label="GAIN 1",min=-10,max=10,steps=20)
    s2=blocks.gui_controls.Slider(label="GAIN 2")
    c1=blocks.gui_controls.CheckBox()
    cntrls = [s1,s2,c1,radio]
    g=GUI(cntrls)
    g.start()
    print("x")


    while(g.is_alive):   
        time.sleep(0.1)
        print("s1={:2.2f}   s2={:2.2f}   c1={}   g={}   ".format(s1.value,s2.value,c1.value,radio.value),end=None)



