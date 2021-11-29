import logging
import numpy as np
from . import exceptions as excpt
from .block import Block
from . import data as data

logger=logging.getLogger(__name__)



class Buffer(Block):
    
    def __init__(self,name:str=None,sz:int=1):
        """
        ### Buffer.  
        converts a serial stream to a buffer.
        
        Data is availible once buffer is full.  
        ### Params  
         - name : descriptive name
         - sz   : size of required buffer
        """
        class_name=self.__class__.__name__
        name=name if name else class_name
        super().__init__(n_max=1,block_class=class_name,name=name)
        self.buffer_sz=sz
        self.data_obj=data.ARRAY_DATA(self.buffer_sz)
        self.data_count=0
        self.data_ready=False



    def run(self,ts):
        self.out_data_valid=False
        if self.data_availible():
            data_obj=self.block_sources[0].out_data_obj
            self.data_obj.data[self.data_count]=data_obj.data
            self.data_count+=1
            if self.data_count==self.buffer_sz:
                self.data_count=0
                self.out_data_valid=True
            else:
                pass
        else:
            pass
       
        return False





class ROLL(Block):
    
    def __init__(self,name:str=None,sz:int=1):
        """
        ### Rolling Buffer.  
        converts a serial stream to a rolling buffer.  
        ### Params  
         - name : descriptive name
         - sz   : size of required buffer
        """
        class_name=self.__class__.__name__
        name=name if name else class_name
        self.buffer_sz=sz
        super().__init__(n_max=1,block_class=class_name,name=name)
        self.data_obj=data.ARRAY_DATA(self.buffer_sz)
    
        self.data_ready=False


    def run(self,ts):
        self.out_data_valid=True
        if self.data_availible():
            data_obj=self.block_sources[0].out_data_obj
            self.data_obj.data=np.roll(self.data_obj.data,1)
            self.data_obj.data[0]=data_obj.data
        else:
            pass
       
        return False
