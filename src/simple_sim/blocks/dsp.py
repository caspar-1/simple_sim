import logging
import numpy as np
from . import exceptions as excpt
from .block import Block
from . import data as data

logger=logging.getLogger(__name__)


class DSP(Block):
    def __init__(self,n_max,block_class,name):
        super().__init__(n_max,block_class,name)

class RATE_CHANGE(DSP):

    def __init__(self,**kwargs):
        name=kwargs.get("name",RATE_CHANGE.__name__)
        super().__init__(n_max=1,block_class=RATE_CHANGE.__name__,name=name)
        self.data_obj=data.STREAM_DATA()
        rate=kwargs.get("rate",2)
        if rate>1:
            self.rate=0
            self.convert_fn=self._convert_up
        else:
            self.rate=int(1/rate)
            self.convert_fn=self._convert_down
        self.count=0

    def _convert_up(self,data_avilible,data):
        if(data_avilible):
            self.data_obj.data=data
        return True

    def _convert_down(self,data_availible,data):
        update=False
        if data_availible:
            if(self.count==0):
                self.count=self.rate-1
                self.data_obj.data=data
                update=True
            else:
                self.count-=1

        return update



    def run(self,ts):
        data_availible=self.data_availible()   
        data_obj=self.block_sources[0].out_data_obj
        self.out_data_valid=self.convert_fn(data_availible,data_obj.data)
        
        return False




class FFT(DSP):
    
    def __init__(self,**kwargs):
        name=kwargs.get("name",FFT.__name__)
        super().__init__(n_max=1,block_class=FFT.__name__,name=name)
        self.data_obj=None
        self._norm=kwargs.get("normalise",False)

    def run(self,ts):    
        
        if self.data_availible():
            data_obj=self.block_sources[0].out_data_obj
            _fft=np.fft.fft(data_obj.data)

            if self._norm:
                sz=(_fft.shape[0])
                _fft=_fft/sz


            if(self.data_obj is None):
                self.data_obj=data.ARRAY_DATA.from_data(_fft)
            else:
                self.data_obj.data=_fft
            self.out_data_valid=True
        else:
            self.out_data_valid=False
   
        return False

class FFT_DISPLAY(DSP):
    def __init__(self,**kwargs):
        name=kwargs.get("name",FFT_DISPLAY.__name__)
        super().__init__(n_max=1,block_class=FFT_DISPLAY.__name__,name=name)
        self._real_f=kwargs.get("real_f",True)
        self._norm=kwargs.get("normalise",True)
        self._abs=kwargs.get("abs",True)

        
    def run(self,ts):    

        
        if self.data_availible():
            _data=self.block_sources[0].out_data_obj.data
            
            if self._real_f:
                sz=(_data.shape[0]//2)
                _data=_data[:-sz]
            else:
                pass

            if self._norm:
                sz=(_data.shape[0])
                _data=_data/sz
                
            if self._abs:
                _data=np.abs(_data)

            if(self.data_obj is None):
                self.data_obj=data.ARRAY_DATA.from_data(_data)
            else:
                self.data_obj.data=_data

            self.out_data_valid=True
        else:
            self.out_data_valid=False

        return False


