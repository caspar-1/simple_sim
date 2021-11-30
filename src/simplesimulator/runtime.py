

import matplotlib.pyplot as plt
import logging
from simplesimulator.misc.key_listener import key_listner
from simplesimulator.custom_exceptions import *
import simplesimulator.misc.function_timer as function_timer
import simplesimulator.blocks  as blocks
import simplesimulator.gui_controls.gui as gui
import simplesimulator.gui_controls as gui_controls
from simplesimulator.blocks.data import ModelState as ms
import os

logging.getLogger('matplotlib.font_manager').disabled = True
logger = logging.getLogger(__name__)


class AbortException(Exception):
    pass

class Model():
    def __init__(self,time_step=1e-3,**kwargs):
        logger.debug("Initialising Runtime Model [Process PID={}]".format(os.getpid()))
        
        self.time = 0.0
        self.ts = time_step
        self.registered_blocks = []
        self.runtime_blocks = []
        self.gui_interface=None
        self.fig = None
        self.axes = None
        self.plot_update=1000
        self.plot_update_count=self.plot_update
        pass

    def create_plot(self, rows, cols, **kwargs):
        plt.ion()
        title = kwargs.get("title", "")
        self.fig, self.axes = plt.subplots(rows, cols)
        self.fig.canvas.set_window_title('Simple Simulator [PID={}]'.format(os.getpid()))
        self.fig.suptitle(title, fontsize=16)
        plt.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)

    def add_block(self, blk):
        if not isinstance(blk, blocks.block.Block):
            raise blocks.exceptions.Block_exception_invalid_class

        self.registered_blocks.append(blk)

    def get_block(self, obj):
        blk = None
        if isinstance(obj, blocks.block.Block):
            name = obj.name
        elif isinstance(obj, str):
            name = obj
        for b in self.registered_blocks:
            if name == b.name:
                blk = b
                break
        return blk

    def link_named(self, source_blk,source_pin, load_blk,load_pin):
        pass

    def link_block(self, source, load):
        _src:blocks.block = self.get_block(source)
        _load:blocks.block = self.get_block(load)

        load_pin_name=None
        source_pin_name=None

        if _src and _load:
            logger.debug("""linking  o/p "{}"---->"{}{}" i/p""".format(_src.name,_load.name,"" if load_pin_name==None else ":{}".format(load_pin_name)))
            _load.add_input(_src)
        else:
            raise blocks.exceptions.Block_exception_add_input_fail

    def init(self):
        logger.debug("model initialisation")
        model_has_dispaly = False
        gui_blocks=[]
        try:
            
            for b in self.registered_blocks:
                if b.check_is_ok()==True:
                    self.runtime_blocks.append(b)
                else:
                    logger.debug("BLOCK {}:{} has no valid inputs".format(b.name,b.block_class))

            
            
            
            for b in self.runtime_blocks:
                if isinstance(b, blocks.display.Display):
                    logger.debug("found display block :{}".format(b.name))
                    model_has_dispaly = True

                if isinstance(b, blocks.gui_blocks.GUI_BLOCK):
                    logger.debug("found gui block :{}".format(b.name))
                    gui_blocks.append(b)

            if len(gui_blocks):
                self.gui_interface=gui.GUI(gui_blocks)

            for b in self.runtime_blocks:
                b.initialise(self)

        except Model_runtime_exception as e:
            logger.error(e)
            raise e
                

    @function_timer.decorator
    def run(self, n=1):
        logger.debug("model run")
        print("Running Model")
        print("Time step  : {}".format(self.ts))
        print("iterations : {}".format(n))
       
        run_aborted=False
        k = key_listner()
        k.start()

        if self.gui_interface:
            self.gui_interface.start(gui_controls.tk_gui_controls.Gui_process_funct)

        for i in range(n):
            update_plots=False
            try:

                if self.gui_interface:
                    if(self.gui_interface.is_alive==False):
                        raise AbortException

                if not k.is_alive():
                    break

                ms.delta=0.0
                ms.time=self.time


                for b in self.runtime_blocks:
                    try:
                        b.pre_run(ms)
                    except:
                        logger.error("failed pre_run :{}".format(b.name))
                

                for b in self.runtime_blocks:
                    try:
                        run_result=b.run(ms)
                        update_plots|=run_result.update_display
                    except:
                        logger.error("failed run :{}".format(b.name))

                for b in self.runtime_blocks:
                    try:
                        b.post_run(ms)
                    except:
                        logger.error("failed post_run :{}".format(b.name))



                if self.plot_update_count!=0:
                    self.plot_update_count-=1

                if self.fig:
                    if not plt.fignum_exists(self.fig.number):
                        raise Model_runtime_exception

                    if ((update_plots) and (self.plot_update_count==0)):
                        self.plot_update_count=self.plot_update
                        self.fig.canvas.draw()
                        self.fig.canvas.flush_events()




            except Model_runtime_exception as e:
                logger.error(e)
                run_aborted=True
                break

            except:
                run_aborted=True
                break

            self.time += self.ts

        for b in self.runtime_blocks:
            b.end_simulation_clean_up()

        
        if self.gui_interface:
            self.gui_interface.stop()
        k.stop()

        msg="simulation ran for {} iterations out of {}  {}".format(i+1,n,"!! RUN Aborted"if run_aborted else "")
        print(msg)
        logger.debug(msg)
