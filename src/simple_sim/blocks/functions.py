import logging
import numpy as np
from . import exceptions as excpt
from .block import Block
from . import data as data

logger=logging.getLogger(__name__)




class Sum(Block):

    def __init__(self,**kwargs):
        name=kwargs.get("name",Sum.__name__)
        super().__init__(n_max=-1,block_class=Sum.__name__,name=name)
        self.data_obj=data.STREAM_DATA()

    def initialise(self):
        logger.debug("initialise {}".format(self.name))
        pass        

    def run(self,ts):
        r=None
        if self.data_availible():
            for i in self.block_sources:
                if r is None:
                    r=i.out_data_obj.data
                else:
                    r=r+i.out_data_obj.data
            self.data_obj.data=r
            self.out_data_valid=True
        else:
            self.out_data_valid=False

        return False

class Sub(Block):
    
    def __init__(self,**kwargs):
        name=kwargs.get("name",Sub.__name__)
        super().__init__(n_max=2,block_class=Sub.__name__,name=name)
        self.data_obj=data.STREAM_DATA()

    def initialise(self):
        logger.debug("initialise {}".format(self.name))
        pass


    def run(self,ts):
        r=None
        if self.data_availible():
            for i in self.block_sources:
                if r is None:
                    r=i.out_data_obj.data
                else:
                    r=r-i.out_data_obj.data

            self.data_obj.data=r
            self.out_data_valid=True
        else:
            self.out_data_valid=False

        return False


class Multiplier(Block):
 
    def __init__(self,**kwargs):
        name=kwargs.get("name",Multiplier.__name__)
        super().__init__(n_max=-1,block_class=Multiplier.__name__,name=name)
        self.data_obj=data.STREAM_DATA()

    def initialise(self):
        logger.debug("initialise {}".format(self.name))
        pass

    def run(self,ts):
        r=None
        if self.data_availible():
            for i in self.block_sources:
                if r is None:
                    r=i.out_data_obj.data
                else:
                    r=r*i.out_data_obj.data

            self.data_obj.data=r
            self.out_data_valid=True
        else:
            self.out_data_valid=False

        return False

    def get_out_data_type(self):
        pass


class ABS(Block):
    
    def __init__(self,**kwargs):
        name=kwargs.get("name",ABS.__name__)
        super().__init__(n_max=1,block_class=ABS.__name__,name=name)
        self.data_obj=data.STREAM_DATA()

    def initialise(self):
        logger.debug("initialise {}".format(self.name))
        pass

    def run(self,ts):
        if self.data_availible():
            data_obj=self.block_sources[0].out_data_obj
            self.data_obj.data=np.abs(data_obj.data)                      
            self.out_data_valid=True
        else:
            self.out_data_valid=False
           
        
        return False



class Buffer(Block):
    
    def __init__(self,**kwargs):
        name=kwargs.get("name",Buffer.__name__)
        self.buffer_sz=kwargs.get("sz",1)
        super().__init__(n_max=1,block_class=Buffer.__name__,name=name)
        self.data_obj=data.ARRAY_DATA(self.buffer_sz)
        self.data_count=0
        self.data_ready=False

    def initialise(self):
        logger.debug("initialise {}".format(self.name))
        pass

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
