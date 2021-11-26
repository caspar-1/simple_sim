from simplesimulator import runtime,blocks
import time
import logging

import simplesimulator.gui_controls as gui_controls



if __name__=="__main__":
    
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S')
    logger=logging.getLogger(__name__)


    s1=blocks.gui_blocks.Gui_slider(label="GAIN 1",min=-10,max=10,steps=20,initial=5)
    s2=blocks.gui_blocks.Gui_slider(label="GAIN 2")
    c1=blocks.gui_blocks.Gui_checkbox(label="check me",initial=False)
    rg=blocks.gui_blocks.Gui_RadioGroup(label="radio group 1",initial=2)
    rg.add_button("a")
    rg.add_button("b")
    rg.add_button("c")
    
    cntrls = [s1,s2,c1,rg]
    g=gui_controls.gui.GUI(cntrls)
    g.start(gui_controls.tk_gui_controls.Gui_process_funct)
 
    while(g.is_alive):   
        time.sleep(0.1)
        print("s1={:2.2f}   s2={:2.2f}  c1={}   rg={}      ".format(s1.value,s2.value,c1.value,rg.value),end='\r')



