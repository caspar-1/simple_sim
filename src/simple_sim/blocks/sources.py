import logging
import numpy as np
from . import exceptions as excpt
from .block import Block

from . import data as data

logger=logging.getLogger(__name__)




class source(Block):
    def __init__(self,n_max,block_class,name):
        super().__init__(n_max,block_class,name)

    def get_out_data_type(self):
        return self.data_obj.data_type




class sine_generator(source):
    
    def __init__(self,**kwargs):
        name=kwargs.get("name",sine_generator.__name__)
        super().__init__(n_max=0,block_class=sine_generator.__name__,name=name)
        self.freq=kwargs.get("freq",1)
        self.apmplitude=kwargs.get("amplitude",1.0)
        self.phase_rads=kwargs.get("phase",0.0)
        self.data_obj=data.STREAM_DATA()

    def run(self,ts):
        self.data_obj.set_data(self.apmplitude*np.sin(2*np.pi*self.freq*ts+self.phase_rads))
        self.out_data_valid=True
        return False




class Noise_generator(source):
    def __init__(self,**kwargs):
        name=kwargs.get("name",Noise_generator.__name__)
        super().__init__(n_max=0,block_class=Noise_generator.__name__,name=name)
        self.apmplitude=kwargs.get("amplitude",1.0)
        self.data_obj=data.STREAM_DATA()

    def run(self,ts):
        self.data_obj.set_data(self.apmplitude*np.random.randn())
        self.out_data_valid=True
        return False



class Random_Digital_generator(source):
    def __init__(self,**kwargs):
        name=kwargs.get("name",Random_Digital_generator.__name__)
        super().__init__(n_max=0,block_class=Random_Digital_generator.__name__,name=name)
        self.nbits=kwargs.get("nbits",8)
        self.data_obj=data.ARRAY_DATA(self.nbits,data_type=data.DATA_TYPES.BOOL)

    def run(self,ts):
        self.data_obj.set_data(np.random.binomial(n=1, p=0.5, size=(self.nbits)))
        self.out_data_valid=True
        return False

   