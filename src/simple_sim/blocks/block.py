import logging
from . import exceptions as excpt


logger=logging.getLogger(__name__)


class Block():
    ID=0
    def __init__(self,n_max,block_class,name=None):
        self.block_sources=[]
        self.block_loads=[]
        self.block_output=None
        self.data=None
        self.out_data=None
        self.n_inputs=0
        self.max_inputs=n_max
        self.block_class=block_class
        self.name="{}_{}".format(block_class,Block.ID) if name is None else name
        Block.ID+=1
        logger.debug("Creating Block :{}".format(self))


    def __del__(self):
        pass

    def add_input(self,blk,**kwargs):
        if not isinstance(blk,Block):
            raise excpt.Block_exception_invalid_class
        if self.n_inputs==self.max_inputs:
            raise excpt.Block_exception_add_input_fail
        self.block_sources.append(blk)
        blk.block_loads.append(self)
        self.n_inputs+=1
    
    
    def initialise(self):
        pass
    
    def run(self)->bool:
        return False

    def update_out_data(self):
        self.out_data=self.data

    def get_data(self):
        return self.out_data

    def get_out_data_type(self):
        raise NotImplementedError

    def end_simulation_clean_up(self):
        pass

    def __repr__(self):
        s="{}:{}:{}".format(self.name,self.block_class,self.out_data)
        return s

