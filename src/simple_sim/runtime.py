

import matplotlib.pyplot as plt
import logging
from simple_sim.key_listner import key_listner
from simple_sim.custom_exceptions import *
import simple_sim.function_timer as function_timer
import simple_sim.blocks  as blocks
import simple_sim.gui as gui


logging.getLogger('matplotlib.font_manager').disabled = True
logger = logging.getLogger(__name__)


class AbortException(Exception):
    pass

class Model():
    def __init__(self,**kwargs):
        self.time = 0.0
        self.ts = kwargs.get("time_step",1e-3)
        self.blocks = []
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
        self.fig.suptitle(title, fontsize=16)

    def add_block(self, blk):
        if not isinstance(blk, blocks.block.Block):
            raise blocks.exceptions.Block_exception_invalid_class

        self.blocks.append(blk)

    def __get_block(self, obj):
        blk = None
        if isinstance(obj, blocks.block.Block):
            name = obj.name
        elif isinstance(obj, str):
            name = obj
        for b in self.blocks:
            if name == b.name:
                blk = b
                break
        return blk

    def link_block(self, source, load):

        def __get(a):
            if isinstance(a, blocks.block.Block):
                blk = a
                pin_name = None
            elif isinstance(a, dict):
                blk = a.get("name", None)
                pin_name = a.get("pin", None)
            elif isinstance(a, str):
                blk = a
                pin_name = None
            else:
                blk = None
                pin_name = None

            return blk,pin_name

        source_blk,source_pin_name=__get(source)
        load_blk,load_pin_name=__get(load)

        _src = self.__get_block(source_blk)
        _load = self.__get_block(load_blk)
        if _src and _load:
            logger.debug("""linking  o/p "{}"---->"{}{}" i/p""".format(_src.name,_load.name,"" if load_pin_name==None else ":{}".format(load_pin_name)))
            _load.add_input(_src,pin_name=load_pin_name)
        else:
            raise blocks.exceptions.Block_exception_add_input_fail

    def init(self):
        logger.debug("model initialisation")
        model_has_dispaly = False
        gui_blocks=[]
        try:
            for b in self.blocks:
                if isinstance(b, blocks.display.Display):
                    logger.debug("found display block :{}".format(b.name))
                    model_has_dispaly = True

                if isinstance(b, blocks.gui_controls.GUI_BLOCK):
                    logger.debug("found gui block :{}".format(b.name))
                    gui_blocks.append(b.gui_obj)

                if b.check_is_ok()==False:
                    raise Model_runtime_exception("BLOCK {}:{} has no valid inputs".format(b.name,b.block_class))

            if model_has_dispaly == True:
                plt.ion()

            if len(gui_blocks):
                self.gui_interface=gui.GUI(gui_blocks)

            for b in self.blocks:
                b.initialise()

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

        if self.gui_interface:
            self.gui_interface.start()


        k.start()
        for i in range(n):
            update_plots=False
            try:
                
                
                if self.gui_interface:
                    if(self.gui_interface.is_running==False):
                        raise AbortException
                
                
                if not k.is_alive():
                    break
                
                try:
                    for b in self.blocks:
                        b.update_out_data()
                except:
                    logger.error("failed update_out_data :{}".format(b.name))

                try:
                    for b in self.blocks:
                        update_plots|=b.run(self.time)
                except:
                    logger.error("failed run :{}".format(b.name))

                try:
                    for b in self.blocks:
                        # print(b)
                        pass
                except:
                    logger.error("failed :{}".format(b.name))
                
                
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

        for b in self.blocks:
            b.end_simulation_clean_up()

        
        if self.gui_interface:
            self.gui_interface.stop()
        k.stop()

        msg="simulation ran for {} iterations out of {}  {}".format(i+1,n,"!! RUN Aborted"if run_aborted else "")
        print(msg)
        logger.debug(msg)
