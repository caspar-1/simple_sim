import logging
import numpy as np
import scipy.signal as signal
from . import exceptions as excpt
from .block import Block,Input,NamedInput
from . import data as data
from .data import ModelState ,RunResult


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



    def run(self,ms:ModelState )->RunResult:
        data_availible=self.data_availible()   
        data_obj=self.block_sources[0].out_data_obj
        self.out_data_valid=self.convert_fn(data_availible,data_obj.data)
        
        return RunResult(False,self.out_data_valid)

class WINDOW(DSP):
    window_dict={"bartlett":np.bartlett,"blackman":np.blackman,"hamming":np.hamming,"hanning":np.hanning}

    
    def __init__(self,name=None,window="hamming",inverse=False):
        class_name = self.__class__.__name__
        name=name if name else class_name
        self.is_inverse=inverse
        super().__init__(n_max=1,block_class=class_name,name=name)
        self.data_obj=None
        self.window=None
        self.window_fnct=WINDOW.window_dict.get(window,np.hamming)

    def run(self,ms:ModelState)->RunResult:
        if self.data_availible():  
            data_in=self.block_sources[0].out_data_obj.data
            if self.window is None:
                if self.is_inverse:
                    self.window=1.0/self.window_fnct(len(data_in))
                else:
                    self.window=self.window_fnct(len(data_in))

            windowed_data=data_in*self.window

            if(self.data_obj is None):
                self.data_obj=data.ARRAY_DATA.from_data(windowed_data)
            else:
                self.data_obj.data=windowed_data

            self.out_data_valid=True
        else:
            self.out_data_valid=False
        
        return RunResult(False,self.out_data_valid)

class FFT(DSP):
    
    def __init__(self,normalise=False,**kwargs):
        name=kwargs.get("name",FFT.__name__)
        super().__init__(n_max=1,block_class=FFT.__name__,name=name)
        self.data_obj=None
        self._norm=normalise

    def run(self,ms:ModelState)->RunResult:    
        
        if self.data_availible():
            data_obj=self.block_sources[0].out_data_obj
            _data=data_obj.data
            
            if self._norm:
                _max=(np.max(_data))
                _data=_data/_max


            data_obj=self.block_sources[0].out_data_obj
            _fft=np.fft.fft(_data)


            if(self.data_obj is None):
                self.data_obj=data.ARRAY_DATA.from_data(_fft)
            else:
                self.data_obj.data=_fft
            self.out_data_valid=True
        else:
            self.out_data_valid=False
   
        return RunResult(False,self.out_data_valid)


class IFFT(DSP):
    
    def __init__(self,**kwargs):
        name=kwargs.get("name",IFFT.__name__)
        super().__init__(n_max=1,block_class=IFFT.__name__,name=name)
        self.data_obj=None

    def run(self,ms:ModelState)->RunResult:    
        
        if self.data_availible():
            data_obj=self.block_sources[0].out_data_obj
            _fft=np.fft.ifft(data_obj.data)

            if(self.data_obj is None):
                self.data_obj=data.ARRAY_DATA.from_data(_fft)
            else:
                self.data_obj.data=_fft
            self.out_data_valid=True
        else:
            self.out_data_valid=False
   
        return RunResult(False,self.out_data_valid)

class FFT_DISPLAY(DSP):
    def __init__(self,**kwargs):
        name=kwargs.get("name",FFT_DISPLAY.__name__)
        super().__init__(n_max=1,block_class=FFT_DISPLAY.__name__,name=name)
        self._real_f=kwargs.get("real_f",True)
        self._norm=kwargs.get("normalise",True)
        self._abs=kwargs.get("abs",True)
        self._log=kwargs.get("log",True)

        
    def run(self,ms:ModelState)->RunResult:    

        
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

            if self._log:
                _data=20*np.log10(_data)

            if(self.data_obj is None):
                self.data_obj=data.ARRAY_DATA.from_data(_data)
            else:
                self.data_obj.data=_data

            self.out_data_valid=True
        else:
            self.out_data_valid=False

        return RunResult(False,self.out_data_valid)


class FILTER_CHEB_LP(DSP):
    
    def __init__(self,**kwargs):
        """
        params:
        - N = Filter order , default=3
        - rp = ripple , default=0.1
        - wp = cut off , default=0.2
        
        """
        name=kwargs.get("name",FILTER_CHEB_LP.__name__)
        super().__init__(n_max=1,block_class=FILTER_CHEB_LP.__name__,name=name)
        self.data_obj=None
        self._n=kwargs.get("N",3)
        self._rp=kwargs.get("rp",0.1)
        self._wn=kwargs.get("wn",0.2)
        

    def initialise(self,model_obj):
        logger.debug("initialise {}".format(self.name))
        super().initialise(model_obj)
        self.sos=signal.cheby1(N=self._n,rp=self._rp,Wn=[self._wn],btype="low",output="sos")
    
    def run(self,ms:ModelState)->RunResult:    
        
        if self.data_availible():
            data_obj=self.block_sources[0].out_data_obj
            _fft=signal.sosfilt(self.sos, data_obj.data)

            if(self.data_obj is None):
                self.data_obj=data.ARRAY_DATA.from_data(_fft)
            else:
                self.data_obj.data=_fft
            self.out_data_valid=True
        else:
            self.out_data_valid=False
   
        return RunResult(False,self.out_data_valid)