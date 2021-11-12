import logging
import numpy as np
from . import exceptions as excpt
from .block import Block
from .data import DATA_TYPES

logger=logging.getLogger(__name__)




class Sum(Block):

    def __init__(self,**kwargs):
        name=kwargs.get("name",Sum.__name__)
        super().__init__(n_max=-1,block_class=Sum.__name__,name=name)
        

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
        name=kwargs.get("name",Sub.__name__)
        super().__init__(n_max=2,block_class=Sub.__name__,name=name)

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
        name=kwargs.get("name",Multiplier.__name__)
        super().__init__(n_max=-1,block_class=Multiplier.__name__,name=name)

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
        name=kwargs.get("name",ABS.__name__)
        super().__init__(n_max=1,block_class=ABS.__name__,name=name)

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
        name=kwargs.get("name",Buffer.__name__)
        self.buffer_sz=kwargs.get("sz",1)
        super().__init__(n_max=1,block_class=Buffer.__name__,name=name)
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
        name=kwargs.get("name",FFT.__name__)
        super().__init__(n_max=1,block_class=FFT.__name__,name=name)
       

    def run(self,ts):    
        
        def __run(data):
            return np.fft.fft(data)

        data=self.block_sources[0].out_data
        if data is None:
            self.data=None
        else:
            self.data=__run(data)
            pass
        
        return False

    def update_out_data(self):
        self.out_data=self.data

class FFT_DISPLAY(Block):
    def __init__(self,**kwargs):
        name=kwargs.get("name",FFT_DISPLAY.__name__)
        super().__init__(n_max=1,block_class=FFT_DISPLAY.__name__,name=name)
        self._real_f=kwargs.get("real_f",True)
        self._norm=kwargs.get("norm",True)
        self._abs=kwargs.get("abs",True)

        
    def run(self,ts):    

        data=self.block_sources[0].out_data
        if data is None:
            self.data=None
        else:
            if self._real_f:
                sz=(data.shape[0]//2)
                self.data=data[:-sz]
            else:
                self.data=data

            if self._norm:
                self.data=self.data/sz
            
            if self._abs:
                self.data=np.abs(self.data)

        return False

    def update_out_data(self):
        self.out_data=self.data



class RATE_CHANGE(Block):


    def __init__(self,**kwargs):
        name=kwargs.get("name",RATE_CHANGE.__name__)
        super().__init__(n_max=1,block_class=RATE_CHANGE.__name__,name=name)
        rate=kwargs.get("rate",2)
        if rate>1:
            self.rate=0
            self.convert_fn=self._convert_up
        else:
            self.rate=int(1/rate)
            self.convert_fn=self._convert_down
        self.count=0

    def _convert_up(self,data):
        if data:
            self.data=data
        else:
            pass

    def _convert_down(self,data):
        if data:
           
            if(self.count==0):
                self.count=self.rate-1
                self.data=data
            else:
                self.count-=1

        else:
            self.data=None



    def run(self,ts):    
        data=self.block_sources[0].out_data
        self.convert_fn(data)

        return False

    def update_out_data(self):
        self.out_data=self.data