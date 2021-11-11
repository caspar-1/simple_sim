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


class Plot(Display):

    def __init__(self, **kwargs):
        super().__init__(n_max=1, block_class=Plot.__name__)
        self.ax = kwargs.get("ax", None)
        self.kwargs = kwargs
        self.line = None

    def initialise(self):
        if self.ax is None:
            self.fig = plt.figure()
            self.ax = self.fig.add_subplot(111)
        else:
            self.fig = self.ax.figure
        self.ax.set_title(self.kwargs.get("title", "Title"))

    def run(self, ts):

        def __run(data):
            try:
                if self.line is None:
                    x = np.linspace(0, 0.5, data.shape[0])
                    self.line, = self.ax.plot(x, data, 'r-')
                else:
                    self.line.set_ydata(data)
            except:
                raise excpt.Model_runtime_exception

        data = self.block_sources[0].out_data
        if data is not None:
            __run(data)
            return True
        return False
