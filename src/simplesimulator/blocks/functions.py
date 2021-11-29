import logging
import numpy as np
from . import exceptions as excpt
from .block import Block,Input,NamedInput
from . import data as data

logger=logging.getLogger(__name__)

class Function_multi_input(Block):

    def __init__(self,name=None):
        cls=self.__class__.__name__
        name=name if name else cls
        super().__init__(n_max=-1,block_class=cls,name=name)
        self.data_obj=data.STREAM_DATA()

    def run(self,ts):
        r=None
        if self.data_availible():
            for i in self.block_sources:
                if r is None:
                    r=i.out_data_obj.data
                else:
                    r=self.func(ts,r,i.out_data_obj.data)

            self.data_obj.data=r
            self.out_data_valid=True
        else:
            self.out_data_valid=False

        return False




class Function_one_input(Block):
    def __init__(self,name=None):
        cls=self.__class__.__name__
        name=name if name else cls
        super().__init__(n_max=1,block_class=cls,name=name)
        self.data_obj=data.STREAM_DATA()

    def run(self,ts):
        if self.data_availible():
            data_obj=self.block_sources[0].out_data_obj
            self.data_obj.data=self.func(ts,data_obj.data)                      
            self.out_data_valid=True
        else:
            self.out_data_valid=False
           
        
        return False


class Sum(Function_multi_input):

    def func(self,ts,r,l):
        return r+l

class Sub(Function_multi_input):
    
    def func(self,ts,r,l):
        return r-l

class Multiplier(Function_multi_input):
 
    def func(self,ts,r,l):
        return r*l

class ABS(Function_one_input):
    
    def func(self,ts,data):
        return np.abs(data) 

class REAL(Function_one_input):
    
    def func(self,ts,data):
        return np.real(data) 

class IMAG(Function_one_input):
    
    def func(self,ts,data):
        return np.imag(data)       

class Recipricol(Function_one_input):
    
    def func(self,ts,data):
        return (1.0/data)       


class Integrate(Function_one_input):
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.integral=0.0
        self.gain=kwargs.get("gain",1.0)
        self.sat_max=kwargs.get("smax",np.finfo.max)
        self.sat_min=kwargs.get("smin",-np.finfo.max)
    
    def func(self,ts,data):
        self.integral+=data*self.gain
        self.integral=self.integral if self.integral<self.sat_max else self.sat_max
        self.integral=self.integral if self.integral>self.sat_min else self.sat_min
        return (self.integral)     


class Differentiate(Function_one_input):
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.z=0.0
        self.gain=kwargs.get("gain",1.0)
        self.sat_max=kwargs.get("smax",np.finfo.max)
        self.sat_min=kwargs.get("smin",-np.finfo.max)
    
    def func(self,ts,data):
        diff=data-self.z
        self.z=data
        
        diff=diff if diff<self.sat_max else self.sat_max
        diff=diff if diff>self.sat_min else self.sat_min
        return (diff)       
          
         
class Switch(Block):

    def __init__(self,name:str=None,select:int=1):
        cls=self.__class__.__name__
        name=name if name else cls
        super().__init__(n_max=-1,block_class=cls,name=name)
        self.data_obj=data.STREAM_DATA()
        self.select_input = NamedInput("select", select)

    def run(self,ts):
        _select = int(self.select_input.get())-1
        self.out_data_valid=False
        if _select<len(self.block_sources):
            source=self.block_sources[_select]
            if source.out_data_valid:
                r=source.out_data_obj.data
                self.data_obj.data=r
                self.out_data_valid=True
          
                

        return False

class Quantize(Function_one_input):
    
    def __init__(self,bits=12,vref=1,**kwargs):
        super().__init__(**kwargs)
        
        self.fsd=2**(bits-1)
        self.vref=vref
    
    def func(self,ts,data):
        d=int((data/self.vref)*self.fsd)
        d=d if d<self.fsd else self.fsd
        d=d if d>-self.fsd else -self.fsd
        return (d)     
