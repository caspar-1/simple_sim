import logging
import numpy as np
from . import exceptions as excpt
from .block import Block
from .data import DATA_TYPES

logger=logging.getLogger(__name__)




class source(Block):
    def __init__(self,n_max,block_class):
        super().__init__(n_max,block_class)


class sine_generator(source):
    
    def __init__(self,**kwargs):
        super().__init__(n_max=0,block_class=sine_generator.__name__)
        self.freq=kwargs.get("freq",1)
        self.apmplitude=kwargs.get("amplitude",1.0)
        self.phase_rads=kwargs.get("phase",0.0)

    def run(self,ts):
        self.data= self.apmplitude*np.sin(2*np.pi*self.freq*ts+self.phase_rads)
        return False

    def get_out_data_type(self):
        return DATA_TYPES.STREAM_DATA



class Noise_generator(source):
    def __init__(self,**kwargs):
        super().__init__(n_max=0,block_class=Noise_generator.__name__)
        self.apmplitude=kwargs.get("amplitude",1.0)

    def run(self,ts):
        self.data= self.apmplitude*np.random.randn()
        return False

    def get_out_data_type(self):
        return DATA_TYPES.STREAM_DATA
