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
    def __init__(self,plot_window,**kwargs):
        if not isinstance(plot_window,Plot_Wndw):
            raise
        name=kwargs.get("name",Line_plot.__name__)
        super().__init__(n_max=1, block_class=Line_plot.__name__,name=name)
        self.plot_window=plot_window
        for k,v in kwargs.items():
            if k in Line_plot.keys_to_pass_to_plot:
                self.plt_args[k]=v
        self.fmt=kwargs.get("fmt","")

        self.line=None
        self.plt_args={}



    def run(self, ts):

        def __run(data):
            try:
                if self.line is None:
                    x = np.linspace(self.plot_window.xlim[0], self.plot_window.xlim[1], data.shape[0])
                    self.line, = self.plot_window.ax.plot(x, data,self.fmt,**self.plt_args)
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
        self.ylim=kwargs.get("ylim",(-1,1))
        self.xlim=kwargs.get("xlim",(0,0.5))
        self.plt_args = dict()
        
        if self.ax is None:
            self.fig = plt.figure()
            self.ax = self.fig.add_subplot(111)
        else:
            self.fig = self.ax.figure
        self.ax.set_title(self.title)
        self.ax.set_ylim(self.ylim)
        
        


    def get_line_plot(self,**kwargs):
        lp=Line_plot(self,**kwargs)
        return lp
