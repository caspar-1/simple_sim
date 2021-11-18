import logging
import numpy as np
import matplotlib.pyplot as plt
from . import exceptions as excpt
from .block import Block
from .data import DATA_TYPES

logger = logging.getLogger(__name__)


class Display(Block):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)





class Line_plot(Display):
    keys_to_pass_to_plot=["drawstyle"]
    def __init__(self,plot,**kwargs):
        if not isinstance(plot,Plot_Wndw):
            raise
        name=kwargs.get("name",Line_plot.__name__)
        super().__init__(n_max=1, block_class=Line_plot.__name__,name=name)
        self.plot=plot
        for k,v in kwargs.items():
            if k in Line_plot.keys_to_pass_to_plot:
                self.plt_args[k]=v
        self.fmt=kwargs.get("fmt","")
        self.line=None
        self.plt_args={}

    def initialise(self):
        logger.debug("initialise {}".format(self.name))
        pass

    def run(self, ts):

        def __run(data):
            try:
                if self.line is None:
                    x = np.linspace(0, 0.5, data.shape[0])
                    self.line, = self.plot.ax.plot(x, data,self.fmt,**self.plt_args)
                else:
                    self.line.set_ydata(data)
            except:
                raise excpt.Model_runtime_exception

        if self.data_availible():
            data_obj = self.block_sources[0].out_data_obj
            if data_obj is not None:
                __run(data_obj.data)
                return True
        return False







class Plot_Wndw(Display):
    keys_to_pass_to_plot=["drawstyle"]

    def __init__(self, ax=None,**kwargs):
        name=kwargs.get("name",Plot_Wndw.__name__)
        super().__init__(n_max=1, block_class=Plot_Wndw.__name__,name=name)
        self.ax = ax
        self.line = None
       
        self.title=kwargs.get("title", "Title")
        self.plt_args = dict()
        #for k,v in kwargs.items():
        #    if k in Plot_Wndw.keys_to_pass_to_plot:
        #        self.plt_args[k]=v

    def initialise(self):
        if self.ax is None:
            self.fig = plt.figure()
            self.ax = self.fig.add_subplot(111)
        else:
            self.fig = self.ax.figure
        self.ax.set_title(self.title)


    def get_line_plot(self,**kwargs):
        lp=Line_plot(self,**kwargs)
        return lp

    def run(self, ts):

        def __run(data):
            try:
                if self.line is None:
                    x = np.linspace(0, 0.5, data.shape[0])
                    self.line, = self.ax.plot(x, data,self.fmt,**self.plt_args)
                else:
                    self.line.set_ydata(data)
            except:
                raise excpt.Model_runtime_exception

        if self.data_availible():
            data_obj = self.block_sources[0].out_data_obj
            if data_obj is not None:
                __run(data_obj.data)
                return True
        return False




