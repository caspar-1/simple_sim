

import matplotlib.pyplot as plt
import logging
from simple_sim.key_listner import key_listner
from simple_sim.custom_exceptions import *
import simple_sim.function_timer as function_timer
import simple_sim.blocks  as blocks


logging.getLogger('matplotlib.font_manager').disabled = True
logger = logging.getLogger(__name__)


class Model():
    def __init__(self,**kwargs):
        self.time = 0.0
        self.ts = kwargs.get("time_step",1e-3)
        self.blocks = []
        self.fig = None
        self.axes = None
        pass

    def create_plot(self, rows, cols, **kwargs):
        plt.ion()
        title = kwargs.get("title", "")
        self.fig, self.axes = plt.subplots(rows, cols)
        self.fig.suptitle(title, fontsize=16)

    def add_block(self, blk):
        if not isinstance(blk, blocks.block.Block):
            raise Block_exception_invalid_class

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
            raise Block_exception_add_input_fail

    def init(self):
        logger.debug("model initialisation")
        model_has_dispaly = False
        for b in self.blocks:
            if isinstance(b, blocks.display.Display):
                model_has_dispaly = True

        if model_has_dispaly == True:
            plt.ion()

        for b in self.blocks:
            b.initialise()

    @function_timer.decorator
    def run(self, n=1):
        logger.debug("model run")
        print("Running Model")
        print("Time step  : {}".format(self.ts))
        print("iterations : {}".format(n))
        k = key_listner()
        k.start()
        for _ in range(n):
            update_plots=False
            try:
                if not k.is_alive():
                    break
                for b in self.blocks:
                    b.update_out_data()
                for b in self.blocks:
                    update_plots|=b.run(self.time)
                for b in self.blocks:
                    # print(b)
                    pass
                
                if self.fig and update_plots:
                    self.fig.canvas.draw()
                    self.fig.canvas.flush_events()
            except Model_runtime_exception:
                break

            except:
                break

            self.time += self.ts

        for b in self.blocks:
            b.end_simulation_clean_up()

        k.stop()
