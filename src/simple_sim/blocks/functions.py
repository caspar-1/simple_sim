import logging
import numpy as np
from . import exceptions as excpt
from .block import Block
from .data import DATA_TYPES

logger=logging.getLogger(__name__)




class Sum(Block):

    def __init__(self,**kwargs):
        super().__init__(n_max=-1,block_class=Sum.__name__)
        

    def run(self,ts):
        r=0.0
        for i in self.block_sources:
            if i.out_data is None:
                r=None
                break
            r=r+i.out_data

        self.data= r
        return False

class Sub(Block):
    
    def __init__(self,**kwargs):
        super().__init__(n_max=2,block_class=Sub.__name__)

    def run(self,ts):
        r=0.0
        a=self.block_sources[0]
        b=self.block_sources[1]
        if a and b:
            r=a.out_data-b.out_data
        else:
            r=None
        self.data= r
        return False


class Multiplier(Block):
 
    def __init__(self,**kwargs):
        super().__init__(n_max=-1,block_class=Multiplier.__name__)

    def run(self,ts):
        r=1.0
        for i in self.block_sources:
            if i.out_data is None:
                r=None
                break
            r=r*i.out_data

        self.data= r
        return False

    def get_out_data_type(self):
        pass


class ABS(Block):
    
    def __init__(self,**kwargs):
        super().__init__(n_max=1,block_class=ABS.__name__)

    def run(self,ts):
        _data=self.block_sources[0].out_data
        if _data is not None:
            r=np.abs(_data)                      
        else:
            r=None
        self.data= r
        return False



class Buffer(Block):
    
    def __init__(self,**kwargs):
        self.buffer_sz=kwargs.get("sz",1)
        super().__init__(n_max=1,block_class=Buffer.__name__)
        self.data=np.zeros(self.buffer_sz)
        self.data_count=0
        self.data_ready=False

    def run(self,ts):
        data=self.block_sources[0].out_data
        if data:
            self.data[self.data_count]=data
            self.data_count+=1
        return False


    def update_out_data(self):
        if self.data_count==self.buffer_sz:
            self.out_data=self.data
            self.data_count=0
        else:
            self.out_data=None

class FFT(Block):
    
    def __init__(self,**kwargs):
        super().__init__(n_max=1,block_class=Buffer.__name__)

    def run(self,ts):    
        
        def __run(data):
            return np.fft.rfft(data)

        data=self.block_sources[0].out_data
        if data is None:
            self.data=None
        else:
            self.data=__run(data)
            pass
        
        return False

    def update_out_data(self):
        self.out_data=self.data